"""CLI: discover, install, inspect, command, gracefully stop, reload."""
import argparse,json,sys,time,datetime,msvcrt
from contextlib import contextmanager
from nxtrainer.transport import Remote
from nxtrainer.runtime import *

STATE=ROOT/'state/active.json'

@contextmanager
def locked():
    path=ROOT/'state/controller.lock'
    path.parent.mkdir(exist_ok=True)
    with path.open('a+b') as handle:
        handle.seek(0);handle.write(b'0');handle.flush();handle.seek(0)
        try:msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
        except OSError:raise RuntimeError('Another trainer command is running')
        try:yield
        finally:handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)

def current():
    require(STATE.exists(),'No recorded trainer session')
    return json.loads(STATE.read_text())

def archive(state):
    atomic_json(ROOT/'state'/('session-'+state['session']+'.json'),state)

def status(remote,profile,state):
    with remote.attached(state['pid']):
        verify_session(remote,state,profile)
        return telemetry(remote,state)

def stop(remote,profile,state):
    require(state['phase']=='active','Use recover for an interrupted transaction')
    with remote.attached(state['pid']):
        verify_session(remote,state,profile)
        values=telemetry(remote,state)
        if values['runtimeStatus']!=2:
            send_command(remote,state,1)
    for _ in range(20):
        time.sleep(.15)
        values=status(remote,profile,state)
        if values['runtimeStatus']==2:break
    else:raise RuntimeError('Cleanup not acknowledged; original bytes retained, no forced restore')
    with remote.attached(state['pid']):
        verify_session(remote,state,profile)
        state['phase']='restoring';atomic_json(STATE,state)
        restore_regions(remote,state['regions'])
        state['phase']='restored';atomic_json(STATE,state);archive(state)
    print('Stopped, effects cleaned up, original RAM restored and verified.')

def install(remote,profile,host):
    payload=Payload(ROOT/'build')
    require(payload.meta['executable_sha256']==profile.fingerprint,'Payload targets another executable')
    candidates=list(applications(remote))
    require(len(candidates)==1,'Expected one running application; launch GTA first')
    pid=candidates[0]
    with remote.attached(pid):
        base=identity(remote);profile.verify(remote,base)
        if STATE.exists():
            old=current()
            if old['pid']!=pid or old['base']!=base:
                old['phase']='expired';archive(old);atomic_json(STATE,old)
            require(old['phase'] in ('restored','expired'),
                    'Existing session journal: stop/reload/recover it before installing')
        target,context,header=find_host(remote,base)
        regions=plan(remote,profile,base,target,context,header,payload)
        state=dict(session=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'),host_ip=host,
                   pid=pid,base=base,host=target,profile=profile.fingerprint,
                   payload_sha256=payload.meta['sha256'],symbols=payload.meta['symbols'],regions=regions)
        apply_transaction(remote,state,STATE)
        archive(state)
    for _ in range(10):
        time.sleep(.15)
        values=status(remote,profile,state)
        if values['runtimeStatus']==1 and values['heartbeat']>0:
            print('Trainer running:',json.dumps(values));return
    raise RuntimeError('Payload installed but heartbeat missing; journal preserved for recovery')

def joaat(text):
    value=0
    for byte in text.lower().encode('ascii'):
        value=(value+byte)&0xffffffff;value=(value+(value<<10))&0xffffffff;value^=value>>6
    value=(value+(value<<3))&0xffffffff;value^=value>>11
    return (value+(value<<15))&0xffffffff

def build_parser():
    parser=argparse.ArgumentParser(description='NX Trainer framework 0.1')
    parser.add_argument('--host',default='192.168.0.122')
    sub=parser.add_subparsers(dest='action',required=True)
    for name in ['discover','install','status','stop','reload','recover','abort-unstarted']:sub.add_parser(name)
    p=sub.add_parser('spawn');p.add_argument('model')
    for name in ['heal','wanted-clear','repair','clean','flip','tune','delete-vehicle',
                 'give-weapons','max-ammo','remove-weapons','parachute','give-heavy',
                 'fix-tyres','stop-vehicle','speed-boost',
                 'clear-peds','clear-vehicles','clear-cops',
                 'customs-extra','appearance-reset','stop-anim',
                 'spoon-attach','spoon-delete',
                 'veh-jump','veh-boost','strike','ragdoll',
                 'bodyguard-spawn','bodyguard-dismiss','add-cash','stunt-ramp',
                 'max-wanted','veh-180','launch-sky','warp-nearest','veh-explode',
                 'online-status','launch-online','host-session']:sub.add_parser(name)
    p=sub.add_parser('drunk');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-wander');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('autopilot');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-siren');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('siren');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('explosion-gun');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-invisible');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('forcefield');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('aim-slowmo');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-drift');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('seatbelt');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-rainbow');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-autorepair');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-hornboost');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-weapons');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('teleport-gun');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('riot-mode');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('veh-fly');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('invincible');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('never-wanted');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('super-jump');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('fast-sprint');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('fast-swim');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('infinite-ammo');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('never-reload');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('explosive-ammo');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('fire-ammo');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('explosive-melee');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('super-damage');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('veh-godmode');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('low-gravity');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('blackout');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('pause-clock');p.add_argument('value',choices=['on','off'])
    p=sub.add_parser('customs-neon');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('customs-neon-color');p.add_argument('color',choices=['white','blue','cyan','electric','mint','green','yellow','pink','red','purple'])
    p=sub.add_parser('customs-tint');p.add_argument('tint',choices=['none','pureblack','darksmoke','lightsmoke','stock','limo'])
    p=sub.add_parser('customs-wheels');p.add_argument('type',choices=['sport','muscle','lowrider','suv','offroad','tuner','bike'])
    p=sub.add_parser('customs-respray');p.add_argument('color',choices=['black','gold','red','blue','green'])
    p=sub.add_parser('appearance-model');p.add_argument('model',choices=['michael','franklin','trevor','mpmale','mpfemale'])
    p=sub.add_parser('appearance-component');p.add_argument('component',type=int,choices=range(0,12),help='Ped component ID (0-11)')
    p=sub.add_parser('play-scenario');p.add_argument('scenario',choices=['smoke','coffee','drinking','cheer','flex','binoculars','pushups','situps','guard'])
    p=sub.add_parser('spoon-object');p.add_argument('model',choices=['cone','barrier','ramp','box'])
    p=sub.add_parser('spoon-freeze');p.add_argument('value',choices=['on','off'],nargs='?',default='on')
    p=sub.add_parser('menu');p.add_argument('value',choices=['open','close'])
    p=sub.add_parser('teleport-forward');p.add_argument('--distance',type=int,default=5)
    p=sub.add_parser('teleport');p.add_argument('destination',choices=['waypoint','michael','franklin','trevor','customs','airport','mazebank','chiliad','zancudo','prison','observatory','sandyshores','paleto','delperro','humane'])
    p=sub.add_parser('time');p.add_argument('value',help='morning, noon, evening, midnight or 0-23')
    p=sub.add_parser('weather');p.add_argument('preset',choices=['extrasunny','clear','clouds','rain','thunder','foggy','snow','reset'])
    return parser

def main():
    parser=build_parser()
    args=parser.parse_args()
    with locked():
        profile=Profile();remote=Remote(args.host)
        try:
            if args.action=='discover':
                candidates=list(applications(remote))
                require(len(candidates)==1,'Expected one running application')
                with remote.attached(candidates[0]):
                    base=identity(remote);profile.verify(remote,base)
                    host,context,header=find_host(remote,base)
                    print(json.dumps(dict(pid=candidates[0],base=hex(base),host=host),indent=2))
            elif args.action=='install':install(remote,profile,args.host)
            else:
                state=current()
                require(state['host_ip']==args.host and state['profile']==profile.fingerprint,'Session host/profile differs')
                if args.action=='status':
                    require(state['phase']=='active','Session is '+state['phase'])
                    print(json.dumps(status(remote,profile,state),indent=2))
                elif args.action in ('stop','reload'):
                    stop(remote,profile,state)
                    if args.action=='reload':install(remote,profile,args.host)
                elif args.action=='menu':
                    require(state['phase']=='active','Trainer is not active')
                    with remote.attached(state['pid']):
                        verify_session(remote,state,profile)
                        values=telemetry(remote,state)
                        require(values['runtimeStatus']==1,'Trainer is stopped; reload it first')
                        address=state['host']['stack']+state['symbols']['menuOpen']*8
                        remote.write(address,struct.pack('<Q',int(args.value=='open')))
                    print('Menu '+args.value)
                elif args.action=='recover':
                    require(state['phase'] in ('prepared','applying','recovery_required','restoring'),
                            'Recovery is only for interrupted writes; active trainer requires graceful stop')
                    with remote.attached(state['pid']):
                        verify_session(remote,state,profile,immutable=False)
                        restore_regions(remote,state['regions'])
                        state['phase']='restored';atomic_json(STATE,state);archive(state)
                    print('Interrupted transaction restored.')
                elif args.action=='abort-unstarted':
                    require(state['phase']=='active','Session is '+state['phase'])
                    with remote.attached(state['pid']):
                        verify_session(remote,state,profile,immutable=False)
                        values=telemetry(remote,state)
                        require(values['runtimeStatus']==0 and values['heartbeat']==0,
                                'Refusing abort: trainer may be running; use stop or inspect status')
                        state['phase']='restoring';atomic_json(STATE,state)
                        restore_regions(remote,state['regions'])
                        state['phase']='restored';atomic_json(STATE,state);archive(state)
                    print('Unstarted payload removed; original RAM restored and verified.')
                else:
                    require(state['phase']=='active','Trainer is not active')
                    if args.action=='online-status':
                        require('networkAccessReason' in state['symbols'],
                                'Active payload lacks network diagnostics; reload the new build during gameplay first')
                    if args.action=='spawn':command,arg=2,joaat(args.model)
                    elif args.action=='heal':command,arg=3,0
                    elif args.action=='wanted-clear':command,arg=4,0
                    elif args.action=='repair':command,arg=5,0
                    elif args.action=='invincible':command,arg=6,int(args.value=='on')
                    elif args.action=='clean':command,arg=10,0
                    elif args.action=='flip':command,arg=11,0
                    elif args.action=='tune':command,arg=12,0
                    elif args.action=='delete-vehicle':command,arg=13,0
                    elif args.action=='teleport':
                        dest_map={'waypoint':(15,0),'michael':(14,0),'franklin':(14,1),'trevor':(14,2),
                                  'customs':(14,3),'airport':(14,4),'mazebank':(14,5),'chiliad':(14,6),
                                  'zancudo':(14,7),'prison':(14,8),'observatory':(14,9),
                                  'sandyshores':(14,10),'paleto':(14,11),'delperro':(14,12),'humane':(14,13)}
                        command,arg=dest_map[args.destination]
                    elif args.action=='teleport-forward':command,arg=50,args.distance
                    elif args.action=='time':
                        time_presets={'morning':8,'noon':12,'evening':18,'midnight':0}
                        hour=time_presets.get(args.value.lower())
                        if hour is None:
                            try:hour=int(args.value)%24
                            except ValueError:raise RuntimeError('Invalid time value: specify morning/noon/evening/midnight or 0-23')
                        command,arg=16,hour
                    elif args.action=='pause-clock':command,arg=17,int(args.value=='on')
                    elif args.action=='weather':
                        w_map={'extrasunny':(18,0),'clear':(18,1),'clouds':(18,2),'rain':(18,3),
                               'thunder':(18,4),'foggy':(18,5),'snow':(18,6),'reset':(19,0)}
                        command,arg=w_map[args.preset]
                    elif args.action=='never-wanted':command,arg=20,int(args.value=='on')
                    elif args.action=='super-jump':command,arg=22,int(args.value=='on')
                    elif args.action=='fast-sprint':command,arg=23,int(args.value=='on')
                    elif args.action=='veh-godmode':command,arg=28,int(args.value=='on')
                    elif args.action=='speed-boost':command,arg=29,0
                    elif args.action=='give-weapons':command,arg=33,0
                    elif args.action=='max-ammo':command,arg=34,0
                    elif args.action=='infinite-ammo':command,arg=35,int(args.value=='on')
                    elif args.action=='never-reload':command,arg=36,int(args.value=='on')
                    elif args.action=='parachute':command,arg=37,0
                    elif args.action=='remove-weapons':command,arg=38,0
                    elif args.action=='blackout':command,arg=39,int(args.value=='on')
                    elif args.action=='fast-swim':command,arg=41,int(args.value=='on')
                    elif args.action=='fix-tyres':command,arg=46,0
                    elif args.action=='stop-vehicle':command,arg=49,0
                    elif args.action=='explosive-ammo':command,arg=51,int(args.value=='on')
                    elif args.action=='fire-ammo':command,arg=52,int(args.value=='on')
                    elif args.action=='explosive-melee':command,arg=53,int(args.value=='on')
                    elif args.action=='super-damage':command,arg=54,int(args.value=='on')
                    elif args.action=='give-heavy':command,arg=55,0
                    elif args.action=='low-gravity':command,arg=56,int(args.value=='on')
                    elif args.action=='clear-peds':command,arg=57,0
                    elif args.action=='clear-vehicles':command,arg=58,0
                    elif args.action=='clear-cops':command,arg=59,0
                    elif args.action=='customs-neon':command,arg=60,int(args.value=='on')
                    elif args.action=='customs-neon-color':
                        neon_colors={'white':0,'blue':1,'cyan':2,'electric':2,'mint':3,'green':3,'yellow':4,'pink':5,'red':6,'purple':7}
                        command,arg=61,neon_colors[args.color]
                    elif args.action=='customs-extra':command,arg=62,0
                    elif args.action=='customs-tint':
                        tint_map={'none':0,'pureblack':1,'darksmoke':2,'lightsmoke':3,'stock':4,'limo':5}
                        command,arg=63,tint_map[args.tint]
                    elif args.action=='customs-wheels':
                        wheel_map={'sport':0,'muscle':1,'lowrider':2,'suv':3,'offroad':4,'tuner':5,'bike':6}
                        command,arg=64,wheel_map[args.type]
                    elif args.action=='customs-respray':
                        respray_map={'black':0,'gold':1,'red':2,'blue':3,'green':4}
                        command,arg=65,respray_map[args.color]
                    elif args.action=='appearance-model':
                        ped_models={'michael':0,'franklin':1,'trevor':2,'mpmale':3,'mpfemale':4}
                        command,arg=66,ped_models[args.model]
                    elif args.action=='appearance-reset':command,arg=67,0
                    elif args.action=='appearance-component':command,arg=68,args.component
                    elif args.action=='play-scenario':
                        scen_map={'smoke':0,'coffee':1,'drinking':1,'cheer':2,'flex':3,'binoculars':4,'pushups':5,'situps':6,'guard':7}
                        command,arg=69,scen_map[args.scenario]
                    elif args.action=='stop-anim':command,arg=70,0
                    elif args.action=='spoon-object':
                        obj_map={'cone':0,'barrier':1,'ramp':2,'box':3}
                        command,arg=71,obj_map[args.model]
                    elif args.action=='spoon-attach':command,arg=72,0
                    elif args.action=='spoon-freeze':command,arg=73,int(args.value=='on')
                    elif args.action=='spoon-delete':command,arg=74,0
                    elif args.action=='veh-jump':command,arg=75,0
                    elif args.action=='veh-drift':command,arg=76,int(args.value=='on')
                    elif args.action=='veh-boost':command,arg=77,0
                    elif args.action=='strike':command,arg=78,0
                    elif args.action=='seatbelt':command,arg=79,int(args.value=='on')
                    elif args.action=='ragdoll':command,arg=80,0
                    elif args.action=='bodyguard-spawn':command,arg=81,0
                    elif args.action=='bodyguard-dismiss':command,arg=82,0
                    elif args.action=='add-cash':command,arg=83,0
                    elif args.action=='stunt-ramp':command,arg=84,0
                    elif args.action=='veh-rainbow':command,arg=85,int(args.value=='on')
                    elif args.action=='veh-autorepair':command,arg=86,int(args.value=='on')
                    elif args.action=='veh-hornboost':command,arg=87,int(args.value=='on')
                    elif args.action=='veh-weapons':command,arg=88,int(args.value=='on')
                    elif args.action=='teleport-gun':command,arg=89,int(args.value=='on')
                    elif args.action=='riot-mode':command,arg=90,int(args.value=='on')
                    elif args.action=='veh-fly':command,arg=91,int(args.value=='on')
                    elif args.action=='explosion-gun':command,arg=92,int(args.value=='on')
                    elif args.action=='max-wanted':command,arg=93,0
                    elif args.action=='veh-invisible':command,arg=94,int(args.value=='on')
                    elif args.action=='veh-180':command,arg=95,0
                    elif args.action=='forcefield':command,arg=96,int(args.value=='on')
                    elif args.action=='aim-slowmo':command,arg=97,int(args.value=='on')
                    elif args.action=='launch-sky':command,arg=98,0
                    elif args.action=='warp-nearest':command,arg=99,0
                    elif args.action=='drunk':command,arg=100,int(args.value=='on')
                    elif args.action in ('veh-wander','autopilot'):command,arg=101,int(args.value=='on')
                    elif args.action in ('veh-siren','siren'):command,arg=102,int(args.value=='on')
                    elif args.action=='veh-explode':command,arg=103,0
                    elif args.action=='online-status':command,arg=8,0
                    elif args.action=='launch-online':command,arg=9,0
                    elif args.action=='host-session':command,arg=9,5
                    else:raise RuntimeError('Unhandled action: '+args.action)
                    with remote.attached(state['pid']):
                        verify_session(remote,state,profile)
                        sequence=send_command(remote,state,command,arg)
                    for _ in range(30):
                        time.sleep(.2)
                        values=status(remote,profile,state)
                        if values['acknowledgedSequence']==sequence and values['pendingModel']==0 and values.get('teleportState',0)==0:
                            print(json.dumps(values,indent=2))
                            if values['lastResult']<0:raise RuntimeError(values['resultLabel'])
                            return
                    raise RuntimeError('Command pending; inspect status before retrying')
        finally:remote.close()

if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,EOFError,ValueError) as error:
        print('ERROR:',error,file=sys.stderr);sys.exit(1)
