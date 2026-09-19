#include "types.h"
#include "constants.h"
#include "intrinsics.h"
#include "natives.h"

/* SC-CL native attribute: low 32 bits first, high 32 bits second. */
extern __attribute((native(0x583051B0,0xAF35D0D2))) Vehicle NX_CREATE(Hash model,vector3 pos,float heading,bool network,bool host,bool p7);
extern __attribute((native(0x3AE6E6A3,0x6B76DC1F))) void NX_HEAL(Entity ped,int health,Entity instigator,Hash weapon);
extern __attribute((native(0xB0D96A57,0xCD015E5B))) void NX_END_TEXT(float x,float y,int flags);
extern __attribute((native(0xCA1E289F,0x3AAD8B2F))) bool NX_TRANSITION_FREEMODE(int* p0,int p1,bool p2,int players,bool p4);
extern __attribute((native(0xBEE4E61D,0x6F3D4ED9))) bool NX_SESSION_HOST(int sessionType,int maxPlayers,bool p2);
extern __attribute((native(0x3497FFCB,0xB0034A22))) bool NX_IS_PAUSE_MENU_ACTIVE();
extern __attribute((native(0x493F1DA5,0x1DD1F58F))) bool NX_IS_WAYPOINT_ACTIVE();
extern __attribute((native(0xE6CD2A1F,0x1BEDE233))) Blip NX_GET_FIRST_BLIP_INFO_ID(int blipSprite);
extern __attribute((native(0xADF25D09,0xFA7C7F0A))) vector3 NX_GET_BLIP_INFO_ID_COORD(Blip blip);
extern __attribute((native(0x9ECBB7DA,0xA6DB27D1))) bool NX_DOES_BLIP_EXIST(Blip blip);
extern __attribute((native(0xB05C8D2B,0xC906A7DA))) bool NX_GET_GROUND_Z(float x,float y,float z,float* groundZ,bool ignoreWater,bool p5);
extern __attribute((native(0x48F491A7,0x07503F79))) void NX_REQUEST_COLLISION_AT_COORD(float x,float y,float z);
extern __attribute((native(0xB4904BDB,0x4448EB75))) bool NX_LOAD_SCENE(float x,float y,float z);
extern __attribute((native(0x060A026B,0x06843DA7))) void NX_SET_ENTITY_COORDS(Entity entity,float xPos,float yPos,float zPos,bool xAxis,bool yAxis,bool zAxis,bool clearArea);
extern __attribute((native(0x8ADA980E,0x8E2530AA))) void NX_SET_ENTITY_HEADING(Entity entity,float heading);
extern __attribute((native(0x726D25D5,0xAB54A438))) void NX_SET_VEHICLE_FORWARD_SPEED(Vehicle vehicle,float speed);
extern __attribute((native(0x9E1C063D,0xF75B0D62))) void NX_SET_PED_INTO_VEHICLE(Ped ped,Vehicle vehicle,int seatIndex);
extern __attribute((native(0xE786A54F,0xEA386986))) void NX_DELETE_VEHICLE(Vehicle* vehicle);
extern __attribute((native(0xB12C0491,0x953DA1E1))) void NX_SET_VEHICLE_DEFORMATION_FIXED(Vehicle vehicle);
extern __attribute((native(0xFE44EE8B,0x79D3B596))) void NX_SET_VEHICLE_DIRT_LEVEL(Vehicle vehicle,float dirtLevel);
extern __attribute((native(0x171D5E07,0x8524A8B0))) void NX_SET_ENTITY_ROTATION(Entity entity,float pitch,float roll,float yaw,int rotationOrder,bool p5);
extern __attribute((native(0x00B3217A,0x1F2AA07F))) void NX_SET_VEHICLE_MOD_KIT(Vehicle vehicle,int modKit);
extern __attribute((native(0xDEDCB6DD,0x6AF0636D))) void NX_SET_VEHICLE_MOD(Vehicle vehicle,int modType,int modIndex,bool customTires);
extern __attribute((native(0xF95BAD08,0x2A1F4F37))) void NX_TOGGLE_VEHICLE_MOD(Vehicle vehicle,int modType,bool toggle);
extern __attribute((native(0xA2500646,0xE38E9162))) int NX_GET_NUM_VEHICLE_MODS(Vehicle vehicle,int modType);
extern __attribute((native(0x8C3E45D8,0x47C3B584))) void NX_SET_CLOCK_TIME(int hours,int minutes,int seconds);
extern __attribute((native(0xD2DBEC1D,0x4055E40B))) void NX_PAUSE_CLOCK(bool toggle);
extern __attribute((native(0x27900C8A,0xED712CA3))) void NX_SET_WEATHER_TYPE_NOW_PERSIST(const char* weatherType);
extern __attribute((native(0xBEF76CF5,0xCCC39339))) void NX_CLEAR_WEATHER_TYPE_PERSIST();
extern __attribute((native(0xDC7BA182,0xB16FCE9D))) bool NX_IS_SCREEN_FADED_OUT();
extern __attribute((native(0x535BA28F,0x797AC7CB))) bool NX_IS_SCREEN_FADING_OUT();
extern __attribute((native(0x8F6E3C5F,0x0DBA7378))) bool NX_IS_DISABLED_CONTROL_PRESSED(int inputGroup,int control);
extern __attribute((native(0x6C964FCB,0xBF0FD6E5))) void NX_GIVE_WEAPON_TO_PED(Ped ped,Hash weaponHash,int ammoCount,bool isHidden,bool equipNow);
extern __attribute((native(0xFA38C5F3,0xF25DF915))) void NX_REMOVE_ALL_PED_WEAPONS(Ped ped,bool p1);
extern __attribute((native(0x5123623B,0x3EDCB050))) void NX_SET_PED_INFINITE_AMMO(Ped ped,bool toggle,Hash weaponHash);
extern __attribute((native(0xAA953186,0x183DADC6))) void NX_SET_PED_INFINITE_AMMO_CLIP(Ped ped,bool toggle);
extern __attribute((native(0x423A4C0B,0x57FFF03E))) void NX_SET_SUPER_JUMP_THIS_FRAME(Player player);
extern __attribute((native(0x7FD94E09,0x6DB47AA7))) void NX_SET_RUN_SPRINT_MULTIPLIER(Player player,float multiplier);
extern __attribute((native(0xA5A45817,0x8FE22675))) void NX_CLEAR_PED_BLOOD_DAMAGE(Ped ped);
extern __attribute((native(0x98F30C05,0x3AC1F7B8))) void NX_RESET_PED_VISIBLE_DAMAGE(Ped ped);
extern __attribute((native(0x04DB6BBB,0xEA1C610A))) void NX_SET_ENTITY_VISIBLE(Entity entity,bool toggle,int unk);
extern __attribute((native(0x56A54E2A,0xB1283770))) void NX_SET_PED_CAN_RAGDOLL(Ped ped,bool toggle);
extern __attribute((native(0x8FFD3681,0x4C7028F7))) void NX_SET_VEHICLE_CAN_BE_VISIBLY_DAMAGED(Vehicle vehicle,bool state);
extern __attribute((native(0xD8596C46,0xEB9DC3C7))) void NX_SET_VEHICLE_TYRES_CAN_BURST(Vehicle vehicle,bool toggle);
extern __attribute((native(0x3C35C862,0x7C65DAC7))) void NX_SET_VEHICLE_DOOR_OPEN(Vehicle vehicle,int doorIndex,bool loose,bool openInstantly);
extern __attribute((native(0xBB013EF5,0x781B3D62))) void NX_SET_VEHICLE_DOORS_SHUT(Vehicle vehicle,bool closeInstantly);
extern __attribute((native(0x43FFB0A1,0x9088EB5A))) void NX_SET_VEHICLE_NUMBER_PLATE_TEXT_INDEX(Vehicle vehicle,int plateIndex);
extern __attribute((native(0xA7F24601,0x4F1D4BE3))) void NX_SET_VEHICLE_COLOURS(Vehicle vehicle,int colorPrimary,int colorSecondary);
extern __attribute((native(0xD440E81E,0x1D408577))) void NX_SET_TIME_SCALE(float timeScale);
extern __attribute((native(0xCE24D504,0x1268615A))) void NX_SET_ARTIFICIAL_LIGHTS_STATE(bool state);
extern __attribute((native(0xF7D16A13,0xA91C6F0F))) void NX_SET_SWIM_MULTIPLIER_FOR_PLAYER(Player player,float multiplier);
extern __attribute((native(0x64CAFD33,0xA352C1B8))) void NX_RESTORE_PLAYER_STAMINA(Player player,float p1);
extern __attribute((native(0x29C2DA6A,0x32C62AA9))) void NX_SET_POLICE_IGNORE_PLAYER(Player player,bool toggle);
extern __attribute((native(0xA5B1F85D,0x18F621F7))) void NX_SET_NIGHTVISION(bool toggle);
extern __attribute((native(0x59E08CE0,0x7E089242))) void NX_SET_SEETHROUGH(bool toggle);
extern __attribute((native(0x8D5F2CFB,0xA66C71C9))) void NX_SET_EXPLOSIVE_AMMO_THIS_FRAME(Player player);
extern __attribute((native(0x803D30F4,0x11879CDD))) void NX_SET_FIRE_AMMO_THIS_FRAME(Player player);
extern __attribute((native(0xBFDC0FE0,0xFF1BED81))) void NX_SET_EXPLOSIVE_MELEE_THIS_FRAME(Player player);
extern __attribute((native(0x817AADA3,0xCE07B9F7))) void NX_SET_PLAYER_WEAPON_DAMAGE_MODIFIER(Player player,float modifier);
extern __attribute((native(0xCC321032,0x4A3DC7EC))) void NX_SET_PLAYER_MELEE_WEAPON_DAMAGE_MODIFIER(Player player,float modifier,bool p2);
extern __attribute((native(0x2B882D1D,0x6E13FC66))) void NX_SET_VEHICLE_TYRE_FIXED(Vehicle vehicle,int tyreIndex);
extern __attribute((native(0x7C8B881E,0x2497C471))) void NX_SET_VEHICLE_ENGINE_ON(Vehicle vehicle,bool value,bool instantly,bool disableAutoStart);
extern __attribute((native(0xD5842351,0x740E14FA))) void NX_SET_GRAVITY_LEVEL(int level);
extern __attribute((native(0xE464AC59,0xBE31FD6C))) void NX_CLEAR_AREA_OF_PEDS(float x,float y,float z,float radius,int flags);
extern __attribute((native(0x8428AEB6,0x01C7B9B3))) void NX_CLEAR_AREA_OF_VEHICLES(float x,float y,float z,float radius,bool p4,bool p5,bool p6,bool p7,bool p8,bool p9,int p10);
extern __attribute((native(0xCF58F88D,0x04F8FC8F))) void NX_CLEAR_AREA_OF_COPS(float x,float y,float z,float radius,int flags);
extern __attribute((native(0x287BF269,0x2AA720E4))) void NX_SET_VEHICLE_NEON_ENABLED(Vehicle vehicle,int index,bool toggle);
extern __attribute((native(0x09A62695,0x8E0A5822))) void NX_SET_VEHICLE_NEON_COLOUR(Vehicle vehicle,int r,int g,int b);
extern __attribute((native(0xE4A40CC9,0x7EE3A3C5))) void NX_SET_VEHICLE_EXTRA(Vehicle vehicle,int extraId,int disable);
extern __attribute((native(0x92428154,0x1262D557))) bool NX_DOES_EXTRA_EXIST(Vehicle vehicle,int extraId);
extern __attribute((native(0x91D15BEA,0x7141766F))) void NX_SET_VEHICLE_CUSTOM_PRIMARY_COLOUR(Vehicle vehicle,int r,int g,int b);
extern __attribute((native(0xFED89754,0x36CED73B))) void NX_SET_VEHICLE_CUSTOM_SECONDARY_COLOUR(Vehicle vehicle,int r,int g,int b);
extern __attribute((native(0xAD752696,0x57C51E6B))) void NX_SET_VEHICLE_WINDOW_TINT(Vehicle vehicle,int tint);
extern __attribute((native(0xC7295BA1,0x487EB21C))) void NX_SET_VEHICLE_WHEEL_TYPE(Vehicle vehicle,int wheelType);
extern __attribute((native(0x00108836,0x00A1CADD))) void NX_SET_PLAYER_MODEL(Player player,Hash model);
extern __attribute((native(0x8D29DE80,0x262B14F4))) void NX_SET_PED_COMPONENT_VARIATION(Ped ped,int componentId,int drawableId,int textureId,int paletteId);
extern __attribute((native(0x732A7842,0x27561561))) int NX_GET_NUMBER_OF_PED_DRAWABLE_VARIATIONS(Ped ped,int componentId);
extern __attribute((native(0x80806D63,0x45EEE615))) void NX_SET_PED_DEFAULT_COMPONENT_VARIATION(Ped ped);
extern __attribute((native(0x5FF02BD9,0x142A0242))) void NX_TASK_START_SCENARIO_IN_PLACE(Ped ped,const char* scenarioName,int unkDelay,bool playEnterAnim);
extern __attribute((native(0x16AFF2CD,0xE1EF3C12))) void NX_CLEAR_PED_TASKS(Ped ped);
extern __attribute((native(0xEB39E842,0x509D5878))) Object NX_CREATE_OBJECT(Hash model,float x,float y,float z,bool isNetwork,bool thisScriptCheck,bool dynamic);
extern __attribute((native(0xAB0796DF,0x6B9BBD38))) void NX_ATTACH_ENTITY_TO_ENTITY(Entity from,Entity to,int boneIndex,float x,float y,float z,float rx,float ry,float rz,bool p9,bool useSoftPinning,bool collision,bool isPed,int rotationOrder,bool syncRot);
extern __attribute((native(0xD1094446,0x428CA6DB))) void NX_FREEZE_ENTITY_POSITION(Entity entity,bool toggle);
extern __attribute((native(0xE6634B9F,0x539E0AE3))) void NX_DELETE_OBJECT(Object* object);
extern __attribute((native(0x613E2D18,0xC5F68BE9))) void NX_APPLY_FORCE_TO_ENTITY(Entity entity,int forceType,float x,float y,float z,float rx,float ry,float rz,int boneIndex,bool isDirectionRel,bool ignoreUpVec,bool isForceRel,bool p12,bool p13);
extern __attribute((native(0x23D122E2,0x222FF6A8))) void NX_SET_VEHICLE_REDUCE_GRIP(Vehicle vehicle,bool toggle);
extern __attribute((native(0xAEE269AC,0xE3AD2BDB))) void NX_ADD_EXPLOSION(float x,float y,float z,int explosionType,float damageScale,bool isAudible,bool isInvisible,float cameraShake);
extern __attribute((native(0x5581844A,0xAE99FB95))) bool NX_SET_PED_TO_RAGDOLL(Ped ped,int time1,int time2,int ragdollType,bool p4,bool p5,bool p6);
extern __attribute((native(0xBF41C463,0x1913FE4C))) void NX_SET_PED_CONFIG_FLAG(Ped ped,int flagId,bool value);
extern __attribute((native(0x37FACADB,0xEF29A163))) Ped NX_CLONE_PED(Ped ped,float heading,bool isNetwork,bool bScriptHostPed);
extern __attribute((native(0xF77030AF,0x0D127585))) int NX_GET_PLAYER_GROUP(Player player);
extern __attribute((native(0x65DB31B5,0x9F3480FE))) void NX_SET_PED_AS_GROUP_MEMBER(Ped ped,int groupId);
extern __attribute((native(0xCB53E54B,0x9614299D))) void NX_DELETE_PED(Ped* ped);
extern __attribute((native(0xB655B441,0xB3271D7A))) bool NX_STAT_SET_INT(Hash statHash,int value,bool save);
extern __attribute((native(0xBA1A2BC2,0x6C4D0409))) bool NX_GET_PED_LAST_WEAPON_IMPACT_COORD(Ped ped,vector3* coords);
extern __attribute((native(0xC7606F2C,0x867654CB))) void NX_SHOOT_SINGLE_BULLET(float x1,float y1,float z1,float x2,float y2,float z2,int damage,bool p7,Hash weapon,Ped ped,bool audible,bool invisible,float speed);
extern __attribute((native(0xC88DFADF,0x2587A48B))) void NX_SET_RIOT_MODE_ENABLED(bool toggle);
extern __attribute((native(0xC4F1689B,0xF73EB622))) Vehicle NX_GET_CLOSEST_VEHICLE(float x,float y,float z,float radius,Hash modelHash,int flags);
extern __attribute((native(0xD5396B8A,0x95D2D383))) void NX_SET_PED_IS_DRUNK(Ped ped,bool toggle);
extern __attribute((native(0x9D337D00,0x48014295))) void NX_TASK_VEHICLE_DRIVE_WANDER(Ped ped,Vehicle vehicle,float speed,int drivingStyle);
extern __attribute((native(0xA19EB37D,0xF4924635))) void NX_SET_VEHICLE_SIREN(Vehicle vehicle,bool toggle);

/* Mailbox ABI: compiler manifest supplies actual static slot numbers. */
int protocolMagic=0x4e585431;
int protocolVersion=1;
int runtimeStatus=0;
int heartbeat=0;
int remoteCommand=0;
int remoteArg=0;
int remoteSequence=0;
int acknowledgedSequence=0;
int lastResult=0;
int lastVehicle=0;
int spawnCount=0;
int networkSignedIn=0;
int networkSignedOnline=0;
int networkCanAccess=0;
int networkAccessReason=-1;
int networkGameInProgress=0;
int networkSessionActive=0;
int selected=0;
int modelIndex=0;
bool menuOpen=false;
bool invincible=false;
Ped previousPed=0;
Hash pendingModel=0;
int requestTime=0;

/* Trainer hierarchical state */
int currentMenu=0;
int categoryIndex=0;
int categoryModelIndex=0;
bool spawnInVehicle=true;
bool spawnTuned=true;
bool spawnGodmode=false;
bool neverWanted=false;
bool superJump=false;
bool fastSprint=false;
bool fastSwim=false;
bool neverTired=false;
bool ignoredByCops=false;
bool thermalVision=false;
bool nightVision=false;
bool invisible=false;
bool noRagdoll=false;
bool vehGodmode=false;
bool engineAlwaysOn=false;
bool doorsOpen=false;
int colorIndex=0;
int plateIndex=0;
bool infiniteAmmo=false;
bool neverReload=false;
bool explosiveAmmo=false;
bool fireAmmo=false;
bool explosiveMelee=false;
bool superDamage=false;
bool clockPaused=false;
bool lowGravity=false;
bool blackout=false;
int timePresetIndex=1;
int weatherPresetIndex=0;
int gameSpeedIndex=0;
int teleportState=0;
int teleportTime=0;
float teleportTargetX=0.0f;
float teleportTargetY=0.0f;
float teleZ=0.0f;
float teleH=0.0f;
float groundZ=0.0f;
int repeatControl=0;
int repeatTimer=0;
RGBA normalColor={230,230,230,255};
RGBA markedColor={255,220,60,255};
vector3 spawnOffset={0.0f,7.0f,0.5f};
vector3 tempPos={0.0f,0.0f,0.0f};
bool neonsOn=false;
int neonColorIndex=0;
int tintIndex=0;
int wheelTypeIndex=0;
int customPaintIndex=0;
int currentExtra=1;
Object lastObject=0;
bool objFrozen=false;
int pedComponentDrawable=0;
bool driftMode=false;
bool seatbelt=false;
Ped lastBodyguard=0;
#define FLAG_RAINBOW      1
#define FLAG_AUTOREPAIR   2
#define FLAG_HORNBOOST    4
#define FLAG_VEHWEAPONS   8
#define FLAG_TELEGUN      16
#define FLAG_RIOTMODE     32
#define FLAG_VEHFLY       64
#define FLAG_EXPLOSIONGUN 128
#define FLAG_VEH_INV      256
#define FLAG_FORCEFIELD   512
#define FLAG_BULLETTIME   1024
#define FLAG_DRUNK        2048
#define FLAG_AUTOPILOT    4096
#define FLAG_SIREN        8192

int extraFlags=0;
int rainbowStep=0;
int menuRow=0;

void toggleFlag(int mask, int arg) {
    if(arg==2)extraFlags^=mask;
    else if(arg!=0)extraFlags|=mask;
    else extraFlags&=~mask;
}

bool toggleVal(bool cur, int arg) {
    if(arg==2)return !cur;
    return arg!=0;
}

void applyRainbowColor(Vehicle veh, int step) {
    int phase = step % 6;
    int r=0,g=0,b=0;
    if(phase<4)r=255;
    if(phase==1)g=165;
    else if(phase==2||phase==3)g=255;
    else if(phase==4){r=128;b=255;}
    else if(phase==5){r=160;g=32;b=240;}
    NX_SET_VEHICLE_CUSTOM_PRIMARY_COLOUR(veh,r,g,b);
    NX_SET_VEHICLE_CUSTOM_SECONDARY_COLOUR(veh,r,g,b);
}
/* Weapon lookups in functions to save static slot array budget */
Hash getArsenalWeapon(int idx) {
    switch(idx) {
        case 0: return 0x1B06D571;
        case 1: return 0x5EF9FEC4;
        case 2: return 0x22D8FE39;
        case 3: return 0x2BE6766B;
        case 4: return 0x13532244;
        case 5: return 0xBFEFFF6D;
        case 6: return 0x83BF0278;
        case 7: return 0xAF113F99;
        case 8: return 0x1D073A89;
        case 9: return 0x7846A318;
        case 10: return 0x05FC3C11;
        case 11: return 0x0C472FE2;
        case 12: return 0xB1CA77B1;
        case 13: return 0xA284510B;
        case 14: return 0x42BF8A46;
        case 15: return 0x2C3731D9;
        case 16: return 0x93E220BD;
        case 17: return 0x24B17070;
        case 18: return 0x99B507EA;
        case 19: return 0x958A4A8F;
        case 20: return 0xFBAB5776;
        default: return 0x2C3731D9;
    }
}

int getCategoryModelCount(int cat) {
    if(cat==0||cat==5)return 2;
    return 1;
}

const char* getCategoryName(int cat) {
    if(cat==0)return "Super";
    if(cat==1)return "Sports";
    if(cat==2)return "Muscle";
    if(cat==3)return "Compact";
    if(cat==4)return "SUV";
    if(cat==5)return "Motorcycle";
    return "Off-Road";
}

const char* getModelName(int cat,int idx) {
    if(cat==0) {
        if(idx==0)return "adder";
        return "zentorno";
    }
    if(cat==1)return "sultan";
    if(cat==2)return "buffalo";
    if(cat==3)return "blista";
    if(cat==4)return "baller";
    if(cat==5) {
        if(idx==0)return "bati";
        return "sanchez";
    }
    return "bifta";
}

const char* getTimePresetName(int idx) {
    if(idx==0)return "Morning";
    if(idx==1)return "Noon";
    if(idx==2)return "Evening";
    return "Midnight";
}

int getTimePresetHour(int idx) {
    if(idx==0)return 8;
    if(idx==1)return 12;
    if(idx==2)return 18;
    return 0;
}

const char* getWeatherPresetDisplayName(int idx) {
    if(idx==0)return "Sunny";
    if(idx==1)return "Clear";
    if(idx==2)return "Clouds";
    if(idx==3)return "Rain";
    if(idx==4)return "Thunder";
    if(idx==5)return "Foggy";
    return "Snow";
}

const char* getWeatherPresetEngineName(int idx) {
    if(idx==0)return "EXTRASUNNY";
    if(idx==1)return "CLEAR";
    if(idx==2)return "CLOUDS";
    if(idx==3)return "RAIN";
    if(idx==4)return "THUNDER";
    if(idx==5)return "FOGGY";
    return "XMAS";
}

const char* getColorName(int idx) {
    if(idx==0)return "Black";
    if(idx==1)return "White";
    if(idx==2)return "Red";
    if(idx==3)return "Blue";
    if(idx==4)return "Green";
    if(idx==5)return "Yellow";
    if(idx==6)return "Orange";
    return "Chrome";
}

int getColorCode(int idx) {
    if(idx==0)return 0;
    if(idx==1)return 111;
    if(idx==2)return 27;
    if(idx==3)return 64;
    if(idx==4)return 55;
    if(idx==5)return 88;
    if(idx==6)return 38;
    return 120;
}

const char* getPlateName(int idx) {
    if(idx==0)return "Blue/White";
    if(idx==1)return "Yellow/Black";
    if(idx==2)return "Yellow/Blue";
    return "SA Exempt";
}

const char* getSpeedName(int idx) {
    if(idx==0)return "Normal";
    if(idx==1)return "0.5x";
    return "0.2x";
}

const char* getNeonColorName(int idx) {
    if(idx==0)return "White";
    if(idx==1)return "Blue";
    if(idx==2)return "Mint";
    if(idx==3)return "Lime";
    if(idx==4)return "Yellow";
    if(idx==5)return "Pink";
    if(idx==6)return "Red";
    return "Purple";
}

const char* getWindowTintName(int idx) {
    if(idx==0)return "None";
    if(idx==1)return "Pure Black";
    if(idx==2)return "Dark Smoke";
    if(idx==3)return "Light Smoke";
    if(idx==4)return "Stock";
    return "Limo";
}

const char* getWheelTypeName(int idx) {
    if(idx==0)return "Sport";
    if(idx==1)return "Muscle";
    if(idx==2)return "Lowrider";
    if(idx==3)return "SUV";
    if(idx==4)return "Offroad";
    if(idx==5)return "Tuner";
    return "High End";
}

const char* getCustomPaintName(int idx) {
    if(idx==0)return "Matte Black";
    if(idx==1)return "Gold";
    if(idx==2)return "Hot Red";
    if(idx==3)return "Electric Blue";
    return "Lime Green";
}

int getMaxRows(int menu) {
    if(menu==0)return 12;
    if(menu==1)return 25;
    if(menu==2)return 28;
    if(menu==3)return 8;
    if(menu==4)return 17;
    if(menu==5)return 15;
    if(menu==6)return 15;
    if(menu==7)return 9;
    if(menu==8)return 9;
    if(menu==9)return 10;
    if(menu==10)return 8;
    return 5;
}

void releasePending() {
    if(pendingModel)SET_MODEL_AS_NO_LONGER_NEEDED(pendingModel);
    pendingModel=0;
}

void deleteLastObject() {
    if(lastObject && DOES_ENTITY_EXIST(lastObject)) {
        NX_DELETE_OBJECT(&lastObject);
        lastObject=0;
    }
}

void deleteLastBodyguard() {
    if(lastBodyguard && DOES_ENTITY_EXIST(lastBodyguard)) {
        NX_DELETE_PED(&lastBodyguard);
        lastBodyguard=0;
    }
}

void cleanup() {
    if(invincible && previousPed && DOES_ENTITY_EXIST(previousPed))SET_ENTITY_INVINCIBLE(previousPed,false);
    invincible=false;
    neverWanted=false;
    superJump=false;
    fastSprint=false;
    fastSwim=false;
    neverTired=false;
    ignoredByCops=false;
    thermalVision=false;
    nightVision=false;
    invisible=false;
    noRagdoll=false;
    vehGodmode=false;
    engineAlwaysOn=false;
    infiniteAmmo=false;
    neverReload=false;
    explosiveAmmo=false;
    fireAmmo=false;
    explosiveMelee=false;
    superDamage=false;
    NX_SET_RUN_SPRINT_MULTIPLIER(PLAYER_ID(),1.0f);
    NX_SET_SWIM_MULTIPLIER_FOR_PLAYER(PLAYER_ID(),1.0f);
    NX_SET_POLICE_IGNORE_PLAYER(PLAYER_ID(),false);
    NX_SET_SEETHROUGH(false);
    NX_SET_NIGHTVISION(false);
    NX_SET_PLAYER_WEAPON_DAMAGE_MODIFIER(PLAYER_ID(),1.0f);
    NX_SET_PLAYER_MELEE_WEAPON_DAMAGE_MODIFIER(PLAYER_ID(),1.0f,false);
    if(previousPed && DOES_ENTITY_EXIST(previousPed)) {
        NX_SET_PED_CAN_RAGDOLL(previousPed,true);
        NX_SET_ENTITY_VISIBLE(previousPed,true,0);
    }
    if(clockPaused) {
        clockPaused=false;
        NX_PAUSE_CLOCK(false);
    }
    if(blackout) {
        blackout=false;
        NX_SET_ARTIFICIAL_LIGHTS_STATE(false);
    }
    if(lowGravity) {
        lowGravity=false;
        NX_SET_GRAVITY_LEVEL(0);
    }
    NX_SET_TIME_SCALE(1.0f);
    NX_CLEAR_WEATHER_TYPE_PERSIST();
    deleteLastObject();
    deleteLastBodyguard();
    if(seatbelt && previousPed && DOES_ENTITY_EXIST(previousPed)) {
        NX_SET_PED_CONFIG_FLAG(previousPed,32,true);
    }
    seatbelt=false;
    driftMode=false;
    if(extraFlags&FLAG_RIOTMODE)NX_SET_RIOT_MODE_ENABLED(false);
    if(extraFlags&FLAG_BULLETTIME)NX_SET_TIME_SCALE(1.0f);
    if((extraFlags&FLAG_DRUNK) && previousPed && DOES_ENTITY_EXIST(previousPed))NX_SET_PED_IS_DRUNK(previousPed,false);
    if((extraFlags&FLAG_AUTOPILOT) && previousPed && DOES_ENTITY_EXIST(previousPed))NX_CLEAR_PED_TASKS(previousPed);
    extraFlags=0;
    releasePending();
    teleportState=0;
    menuOpen=false;
    lastResult=7;
    runtimeStatus=2;
}

bool loadModelSync(Hash model) {
    if(!IS_MODEL_IN_CDIMAGE(model))return false;
    REQUEST_MODEL(model);
    int timer=GET_GAME_TIMER()+2000;
    while(!HAS_MODEL_LOADED(model) && GET_GAME_TIMER()<timer)WAIT(0);
    return HAS_MODEL_LOADED(model);
}

void requestVehicle(Hash model) {
    if(pendingModel) {lastResult=-6;return;}
    if(!IS_MODEL_IN_CDIMAGE(model) || !IS_MODEL_A_VEHICLE(model)) {lastResult=-2;return;}
    pendingModel=model;
    requestTime=GET_GAME_TIMER();
    lastResult=1;
    REQUEST_MODEL(model);
}

void maxTuneVehicle(Vehicle veh) {
    NX_SET_VEHICLE_MOD_KIT(veh,0);
    for(int m=11;m<=16;m++) {
        int count=NX_GET_NUM_VEHICLE_MODS(veh,m);
        if(count>0)NX_SET_VEHICLE_MOD(veh,m,count-1,false);
    }
    NX_TOGGLE_VEHICLE_MOD(veh,18,true);
}

void updateVehicle(Ped ped) {
    if(!pendingModel)return;
    if(HAS_MODEL_LOADED(pendingModel)) {
        tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(ped,spawnOffset);
        Vehicle vehicle=NX_CREATE(pendingModel,tempPos,GET_ENTITY_HEADING(ped),false,false,false);
        if(vehicle && DOES_ENTITY_EXIST(vehicle)) {
            SET_VEHICLE_ON_GROUND_PROPERLY(vehicle,5.0f);
            if(spawnTuned)maxTuneVehicle(vehicle);
            if(spawnGodmode) {
                SET_ENTITY_INVINCIBLE(vehicle,true);
                NX_SET_VEHICLE_CAN_BE_VISIBLY_DAMAGED(vehicle,false);
                NX_SET_VEHICLE_TYRES_CAN_BURST(vehicle,false);
            }
            if(spawnInVehicle) {
                NX_SET_PED_INTO_VEHICLE(ped,vehicle,-1);
            }
            lastVehicle=vehicle;
            spawnCount++;
            lastResult=2;
            SET_VEHICLE_AS_NO_LONGER_NEEDED(&vehicle);
        } else {lastResult=-4;}
        releasePending();
    } else if(GET_GAME_TIMER()-requestTime>5000) {
        releasePending();lastResult=-3;
    }
}

void updateTeleport(Ped ped) {
    if(teleportState==0)return;
    Entity ent=ped;
    if(IS_PED_IN_ANY_VEHICLE(ped,false))ent=GET_VEHICLE_PED_IS_IN(ped,false);
    if(!DOES_ENTITY_EXIST(ent)) {teleportState=0;return;}

    bool found=false;
    for(float z=50.0f; z<=800.0f; z+=150.0f) {
        if(NX_GET_GROUND_Z(teleportTargetX,teleportTargetY,z,&groundZ,false,false)) {
            found=true;
            break;
        }
    }

    if(found) {
        teleportState=0;
        NX_SET_ENTITY_COORDS(ent,teleportTargetX,teleportTargetY,groundZ+1.0f,false,false,false,true);
        if(ent!=ped) {
            SET_VEHICLE_ON_GROUND_PROPERLY(ent,5.0f);
            NX_SET_VEHICLE_FORWARD_SPEED(ent,0.0f);
        }
        lastResult=13;
    } else if(GET_GAME_TIMER()-teleportTime>3500) {
        teleportState=0;
        lastResult=-13;
    }
}

void setTele(float x,float y,float z,float h) {
    teleportTargetX=x;teleportTargetY=y;teleZ=z;teleH=h;
}

void setTeleportLocation(int idx) {
    if(idx==0)setTele(-813.88f,178.68f,72.15f,110.0f);
    else if(idx==1)setTele(7.9f,529.8f,170.6f,290.0f);
    else if(idx==2)setTele(1975.2f,3817.3f,33.4f,30.0f);
    else if(idx==3)setTele(-365.4f,-131.8f,38.7f,70.0f);
    else if(idx==4)setTele(-1034.6f,-2733.6f,13.8f,330.0f);
    else if(idx==5)setTele(-75.0f,-818.5f,326.0f,330.0f);
    else if(idx==6)setTele(501.5f,5604.5f,797.9f,355.0f);
    else if(idx==7)setTele(-2047.4f,3132.1f,32.8f,150.0f);
    else if(idx==8)setTele(1846.4f,2585.9f,45.7f,90.0f);
    else if(idx==9)setTele(-438.4f,1072.8f,327.7f,340.0f);
    else if(idx==10)setTele(1747.0f,3273.0f,41.1f,190.0f);
    else if(idx==11)setTele(-106.0f,6467.0f,31.6f,45.0f);
    else if(idx==12)setTele(-1686.0f,-1072.0f,13.1f,50.0f);
    else setTele(3616.0f,3737.0f,28.7f,270.0f);
}

void teleportEntity(Entity ent) {
    NX_LOAD_SCENE(teleportTargetX,teleportTargetY,teleZ);
    NX_REQUEST_COLLISION_AT_COORD(teleportTargetX,teleportTargetY,teleZ);
    NX_SET_ENTITY_COORDS(ent,teleportTargetX,teleportTargetY,teleZ,false,false,false,true);
    NX_SET_ENTITY_HEADING(ent,teleH);
    if(ent!=PLAYER_PED_ID()) {
        SET_VEHICLE_ON_GROUND_PROPERLY(ent,5.0f);
        NX_SET_VEHICLE_FORWARD_SPEED(ent,0.0f);
    }
}

void action(int command,int argument) {
    if(command==1) {cleanup();return;}
    if(command==8) {
        networkSignedIn=NETWORK_IS_SIGNED_IN();
        networkSignedOnline=NETWORK_IS_SIGNED_ONLINE();
        networkAccessReason=-1;
        networkCanAccess=NETWORK_CAN_ACCESS_MULTIPLAYER(&networkAccessReason);
        networkGameInProgress=NETWORK_IS_GAME_IN_PROGRESS();
        networkSessionActive=NETWORK_IS_SESSION_ACTIVE();
        lastResult=8;return;
    }
    Ped ped=PLAYER_PED_ID();
    if(command==9) {
        if(argument==0) {
            networkSignedIn=NETWORK_IS_SIGNED_IN();
            networkSignedOnline=NETWORK_IS_SIGNED_ONLINE();
            networkAccessReason=-1;
            networkCanAccess=NETWORK_CAN_ACCESS_MULTIPLAYER(&networkAccessReason);
            if(!networkSignedIn || !networkSignedOnline || !networkCanAccess) {
                lastResult=-49;return;
            }
            bool ok=NX_TRANSITION_FREEMODE(0,0,true,32,false);
            lastResult=ok?9:-39;
        } else if(argument==1) {
            bool ok=NX_SESSION_HOST(1,32,false);
            lastResult=ok?10:-10;
        } else if(argument==5) {
            bool ok=NX_SESSION_HOST(5,32,false);
            lastResult=ok?11:-11;
        }
        return;
    }
    if(!DOES_ENTITY_EXIST(ped) || IS_ENTITY_DEAD(ped)) {lastResult=-1;return;}
    Vehicle v = IS_PED_IN_ANY_VEHICLE(ped,false) ? GET_VEHICLE_PED_IS_IN(ped,false) : 0;
    if(!v) {
        if(command==5 || (command>=10 && command<=12) || (command>=29 && command<=32) || command==46 || command==48 || command==49 || (command>=60 && command<=65) || (command>=75 && command<=77) || command==95 || command==101 || command==102) {
            lastResult=-5;
            return;
        }
    }
    if(command==2)requestVehicle(argument);
    if(command==3) {NX_HEAL(ped,GET_ENTITY_MAX_HEALTH(ped),0,0);SET_PED_ARMOUR(ped,100);lastResult=3;}
    if(command==4) {SET_PLAYER_WANTED_LEVEL(PLAYER_ID(),0,false);SET_PLAYER_WANTED_LEVEL_NOW(PLAYER_ID(),false);lastResult=4;}
    if(command==5) {
        SET_VEHICLE_FIXED(v);
        NX_SET_VEHICLE_DEFORMATION_FIXED(v);
        NX_SET_VEHICLE_DIRT_LEVEL(v,0.0f);
        lastResult=5;
    }
    if(command==6) {invincible=toggleVal(invincible,argument);SET_ENTITY_INVINCIBLE(ped,invincible);lastResult=6;}
    if(command==10) {
        NX_SET_VEHICLE_DIRT_LEVEL(v,0.0f);
        lastResult=14;
    }
    if(command==11) {
        float h=GET_ENTITY_HEADING(v);
        NX_SET_ENTITY_ROTATION(v,0.0f,0.0f,h,2,true);
        SET_VEHICLE_ON_GROUND_PROPERLY(v,5.0f);
        lastResult=15;
    }
    if(command==12) {
        maxTuneVehicle(v);
        lastResult=16;
    }
    if(command==13) {
        if(lastVehicle && DOES_ENTITY_EXIST(lastVehicle)) {
            NX_DELETE_VEHICLE(&lastVehicle);
            lastVehicle=0;
            lastResult=17;
        } else lastResult=-5;
    }
    if(command==14) {
        setTeleportLocation(argument);
        Entity ent=v?v:ped;
        teleportEntity(ent);
        lastResult=13;
    }
    if(command==15) {
        if(!NX_IS_WAYPOINT_ACTIVE()) {lastResult=-12;return;}
        Blip wpBlip=NX_GET_FIRST_BLIP_INFO_ID(8);
        if(!NX_DOES_BLIP_EXIST(wpBlip)) {lastResult=-12;return;}
        vector3 wp=NX_GET_BLIP_INFO_ID_COORD(wpBlip);
        teleportTargetX=wp.x;
        teleportTargetY=wp.y;
        teleportState=1;
        teleportTime=GET_GAME_TIMER();
        NX_REQUEST_COLLISION_AT_COORD(wp.x,wp.y,100.0f);
        NX_LOAD_SCENE(wp.x,wp.y,100.0f);
        lastResult=12;
    }
    if(command==16) {NX_SET_CLOCK_TIME(argument,0,0);lastResult=18;}
    if(command==17) {clockPaused=argument!=0;NX_PAUSE_CLOCK(clockPaused);lastResult=18;}
    if(command==18) {NX_SET_WEATHER_TYPE_NOW_PERSIST(getWeatherPresetEngineName(argument));lastResult=19;}
    if(command==19) {NX_CLEAR_WEATHER_TYPE_PERSIST();lastResult=20;}
    if(command==20) {neverWanted=toggleVal(neverWanted,argument);lastResult=neverWanted?21:22;}
    if(command==21) {spawnInVehicle=argument!=0;}
    if(command==22) {superJump=toggleVal(superJump,argument);}
    if(command==23) {
        fastSprint=toggleVal(fastSprint,argument);
        NX_SET_RUN_SPRINT_MULTIPLIER(PLAYER_ID(),fastSprint?1.49f:1.0f);
    }
    if(command==24) {
        NX_CLEAR_PED_BLOOD_DAMAGE(ped);
        NX_RESET_PED_VISIBLE_DAMAGE(ped);
        lastResult=24;
    }
    if(command==25) {
        invisible=toggleVal(invisible,argument);
        NX_SET_ENTITY_VISIBLE(ped,!invisible,0);
        lastResult=25;
    }
    if(command==26) {
        noRagdoll=toggleVal(noRagdoll,argument);
        NX_SET_PED_CAN_RAGDOLL(ped,!noRagdoll);
        lastResult=26;
    }
    if(command==27) {NX_HEAL(ped,0,0,0);lastResult=27;} // Suicide
    if(command==28) {
        vehGodmode=toggleVal(vehGodmode,argument);
        if(v) {
            SET_ENTITY_INVINCIBLE(v,vehGodmode);
            NX_SET_VEHICLE_CAN_BE_VISIBLY_DAMAGED(v,!vehGodmode);
            NX_SET_VEHICLE_TYRES_CAN_BURST(v,!vehGodmode);
        }
        lastResult=28;
    }
    if(command==29) {
        NX_SET_VEHICLE_FORWARD_SPEED(v,35.0f);
        lastResult=29;
    }
    if(command==30) {
        doorsOpen=!doorsOpen;
        if(doorsOpen) {
            NX_SET_VEHICLE_DOOR_OPEN(v,0,false,false);
            NX_SET_VEHICLE_DOOR_OPEN(v,1,false,false);
        } else {
            NX_SET_VEHICLE_DOORS_SHUT(v,false);
        }
        lastResult=30;
    }
    if(command==31) {
        int code=getColorCode(argument);
        NX_SET_VEHICLE_COLOURS(v,code,code);
        lastResult=31;
    }
    if(command==32) {
        NX_SET_VEHICLE_NUMBER_PLATE_TEXT_INDEX(v,argument);
        lastResult=32;
    }
    if(command==33 || command==34) {
        int cnt=(command==33)?21:20;
        for(int w=0;w<cnt;w++) {
            NX_GIVE_WEAPON_TO_PED(ped,getArsenalWeapon(w),9999,false,false);
        }
        lastResult=command;
    }
    if(command==35) {
        infiniteAmmo=toggleVal(infiniteAmmo,argument);
        NX_SET_PED_INFINITE_AMMO(ped,infiniteAmmo,0);
        NX_SET_PED_INFINITE_AMMO_CLIP(ped,infiniteAmmo);
        lastResult=35;
    }
    if(command==36) {
        neverReload=toggleVal(neverReload,argument);
        NX_SET_PED_INFINITE_AMMO_CLIP(ped,neverReload);
        lastResult=36;
    }
    if(command==37) {
        NX_GIVE_WEAPON_TO_PED(ped,0xFBAB5776,1,false,true);
        lastResult=37;
    }
    if(command==38) {
        NX_REMOVE_ALL_PED_WEAPONS(ped,true);
        lastResult=38;
    }
    if(command==39) {
        blackout=toggleVal(blackout,argument);
        NX_SET_ARTIFICIAL_LIGHTS_STATE(blackout);
        lastResult=39;
    }
    if(command==40) {
        float spd=1.0f;
        if(argument==1)spd=0.5f;
        else if(argument==2)spd=0.2f;
        NX_SET_TIME_SCALE(spd);
        lastResult=40;
    }
    if(command==41) {
        fastSwim=toggleVal(fastSwim,argument);
        NX_SET_SWIM_MULTIPLIER_FOR_PLAYER(PLAYER_ID(),fastSwim?1.49f:1.0f);
        lastResult=41;
    }
    if(command==42) {
        neverTired=toggleVal(neverTired,argument);
        lastResult=42;
    }
    if(command==43) {
        ignoredByCops=toggleVal(ignoredByCops,argument);
        NX_SET_POLICE_IGNORE_PLAYER(PLAYER_ID(),ignoredByCops);
        lastResult=43;
    }
    if(command==44) {
        thermalVision=toggleVal(thermalVision,argument);
        NX_SET_SEETHROUGH(thermalVision);
        lastResult=44;
    }
    if(command==45) {
        nightVision=toggleVal(nightVision,argument);
        NX_SET_NIGHTVISION(nightVision);
        lastResult=45;
    }
    if(command==46) {
        for(int t=0;t<8;t++)NX_SET_VEHICLE_TYRE_FIXED(v,t);
        lastResult=46;
    }
    if(command==47) {
        engineAlwaysOn=toggleVal(engineAlwaysOn,argument);
        lastResult=47;
    }
    if(command==48) {
        NX_SET_VEHICLE_TYRES_CAN_BURST(v,false);
        lastResult=48;
    }
    if(command==49) {
        NX_SET_VEHICLE_FORWARD_SPEED(v,0.0f);
        lastResult=49;
    }
    if(command==50) {
        Entity ent=v?v:ped;
        tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(ent,spawnOffset);
        NX_SET_ENTITY_COORDS(ent,tempPos.x,tempPos.y,tempPos.z,false,false,false,true);
        lastResult=50;
    }
    if(command==51) {
        explosiveAmmo=toggleVal(explosiveAmmo,argument);
        lastResult=51;
    }
    if(command==52) {
        fireAmmo=toggleVal(fireAmmo,argument);
        lastResult=52;
    }
    if(command==53) {
        explosiveMelee=toggleVal(explosiveMelee,argument);
        lastResult=53;
    }
    if(command==54) {
        superDamage=toggleVal(superDamage,argument);
        float mod=superDamage?999.0f:1.0f;
        NX_SET_PLAYER_WEAPON_DAMAGE_MODIFIER(PLAYER_ID(),mod);
        NX_SET_PLAYER_MELEE_WEAPON_DAMAGE_MODIFIER(PLAYER_ID(),mod,false);
        lastResult=54;
    }
    if(command==55) {
        for(int h=11;h<=15;h++)NX_GIVE_WEAPON_TO_PED(ped,getArsenalWeapon(h),9999,false,false);
        NX_GIVE_WEAPON_TO_PED(ped,0x63AB0442,9999,false,false);
        lastResult=55;
    }
    if(command==56) {
        lowGravity=toggleVal(lowGravity,argument);
        NX_SET_GRAVITY_LEVEL(lowGravity?1:0);
        lastResult=56;
    }
    if(command>=57 && command<=59) {
        tempPos=GET_ENTITY_COORDS(ped,true);
        if(command==57)NX_CLEAR_AREA_OF_PEDS(tempPos.x,tempPos.y,tempPos.z,200.0f,1);
        else if(command==58)NX_CLEAR_AREA_OF_VEHICLES(tempPos.x,tempPos.y,tempPos.z,200.0f,false,false,false,false,false,false,0);
        else NX_CLEAR_AREA_OF_COPS(tempPos.x,tempPos.y,tempPos.z,200.0f,0);
        lastResult=command;
    }
    if(command==60) {
        if(argument==2)neonsOn=!neonsOn;
        else neonsOn=argument!=0;
        for(int n=0;n<4;n++)NX_SET_VEHICLE_NEON_ENABLED(v,n,neonsOn);
        lastResult=60;
    }
    if(command==61) {
        neonColorIndex=argument%8;
        int r=255,g=255,b=255;
        if(neonColorIndex==1){r=0;g=0;b=255;}
        else if(neonColorIndex==2){r=0;g=255;b=180;}
        else if(neonColorIndex==3){r=50;g=255;b=0;}
        else if(neonColorIndex==4){r=255;g=255;b=0;}
        else if(neonColorIndex==5){r=255;g=50;b=200;}
        else if(neonColorIndex==6){r=255;g=0;b=0;}
        else if(neonColorIndex==7){r=150;g=0;b=255;}
        NX_SET_VEHICLE_NEON_COLOUR(v,r,g,b);
        lastResult=61;
    }
    if(command==62) {
        currentExtra=(currentExtra%6)+1;
        if(NX_DOES_EXTRA_EXIST(v,currentExtra)) {
            NX_SET_VEHICLE_EXTRA(v,currentExtra,0);
        }
        lastResult=62;
    }
    if(command==63) {
        tintIndex=argument%6;
        NX_SET_VEHICLE_WINDOW_TINT(v,tintIndex);
        lastResult=63;
    }
    if(command==64) {
        wheelTypeIndex=argument%7;
        NX_SET_VEHICLE_WHEEL_TYPE(v,wheelTypeIndex);
        lastResult=64;
    }
    if(command==65) {
        customPaintIndex=argument%5;
        int r=0,g=0,b=0;
        if(customPaintIndex==1){r=218;g=165;b=32;}
        else if(customPaintIndex==2){r=255;g=10;b=10;}
        else if(customPaintIndex==3){r=0;g=120;b=255;}
        else if(customPaintIndex==4){r=100;g=255;b=0;}
        NX_SET_VEHICLE_CUSTOM_PRIMARY_COLOUR(v,r,g,b);
        NX_SET_VEHICLE_CUSTOM_SECONDARY_COLOUR(v,r,g,b);
        lastResult=65;
    }
    if(command==66) {
        Hash model=0x9B22DBAF;
        if(argument==0)model=0x0D7114C9;
        else if(argument==1)model=0x9B22DBAF;
        else if(argument==2)model=0x9B810FA2;
        else if(argument==3)model=0x705E61F2;
        else if(argument==4)model=0x9C9EFFD8;
        if(loadModelSync(model)) {
            NX_SET_PLAYER_MODEL(PLAYER_ID(),model);
            SET_MODEL_AS_NO_LONGER_NEEDED(model);
            lastResult=66;
        } else lastResult=-3;
    }
    if(command==67) {
        NX_SET_PED_DEFAULT_COMPONENT_VARIATION(ped);
        lastResult=67;
    }
    if(command==68) {
        pedComponentDrawable++;
        int maxD=NX_GET_NUMBER_OF_PED_DRAWABLE_VARIATIONS(ped,argument);
        if(maxD>0) {
            pedComponentDrawable=pedComponentDrawable%maxD;
            NX_SET_PED_COMPONENT_VARIATION(ped,argument,pedComponentDrawable,0,0);
        }
        lastResult=68;
    }
    if(command==69) {
        const char* scen="WORLD_HUMAN_SMOKING";
        if(argument==1)scen="WORLD_HUMAN_DRINKING";
        else if(argument==2)scen="WORLD_HUMAN_CHEERING";
        else if(argument==3)scen="WORLD_HUMAN_MUSCLE_FLEX";
        else if(argument==4)scen="WORLD_HUMAN_BINOCULARS";
        else if(argument==5)scen="WORLD_HUMAN_PUSH_UPS";
        else if(argument==6)scen="WORLD_HUMAN_SIT_UPS";
        else if(argument==7)scen="WORLD_HUMAN_GUARD_STAND";
        NX_CLEAR_PED_TASKS(ped);
        NX_TASK_START_SCENARIO_IN_PLACE(ped,scen,0,true);
        lastResult=69;
    }
    if(command==70) {
        NX_CLEAR_PED_TASKS(ped);
        lastResult=70;
    }
    if(command==71) {
        Hash objModel=0xC2339364;
        if(argument==1)objModel=0xF7752D66;
        else if(argument==2)objModel=0xB157C9E4;
        else if(argument==3)objModel=0x9109DFBC;
        if(loadModelSync(objModel)) {
            tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(ped,spawnOffset);
            deleteLastObject();
            lastObject=NX_CREATE_OBJECT(objModel,tempPos.x,tempPos.y,tempPos.z,false,false,false);
            SET_MODEL_AS_NO_LONGER_NEEDED(objModel);
            objFrozen=false;
            lastResult=71;
        } else lastResult=-3;
    }
    if(command==72) {
        if(lastObject && DOES_ENTITY_EXIST(lastObject)) {
            NX_ATTACH_ENTITY_TO_ENTITY(lastObject,ped,0,0.0f,1.5f,0.2f,0.0f,0.0f,0.0f,false,false,false,false,2,true);
            lastResult=72;
        } else lastResult=-4;
    }
    if(command==73) {
        if(lastObject && DOES_ENTITY_EXIST(lastObject)) {
            if(argument==2)objFrozen=!objFrozen;
            else objFrozen=argument!=0;
            NX_FREEZE_ENTITY_POSITION(lastObject,objFrozen);
            lastResult=73;
        } else lastResult=-4;
    }
    if(command==74) {
        if(lastObject) {
            deleteLastObject();
            lastResult=74;
        } else lastResult=-4;
    }
    if(command==75) {
        NX_APPLY_FORCE_TO_ENTITY(v,1,0.0f,0.0f,11.0f,0.0f,0.0f,0.0f,0,true,true,true,false,true);
        lastResult=75;
    }
    if(command==76) {
        if(argument==2)driftMode=!driftMode;
        else driftMode=argument!=0;
        NX_SET_VEHICLE_REDUCE_GRIP(v,driftMode);
        lastResult=76;
    }
    if(command==77) {
        NX_SET_VEHICLE_FORWARD_SPEED(v,70.0f);
        lastResult=77;
    }
    if(command==78) {
        spawnOffset.x=0.0f; spawnOffset.y=18.0f; spawnOffset.z=0.0f;
        tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(ped,spawnOffset);
        spawnOffset.x=0.0f; spawnOffset.y=7.0f; spawnOffset.z=0.5f;
        NX_ADD_EXPLOSION(tempPos.x,tempPos.y,tempPos.z,29,10.0f,true,false,2.0f);
        lastResult=78;
    }
    if(command==79) {
        if(argument==2)seatbelt=!seatbelt;
        else seatbelt=argument!=0;
        NX_SET_PED_CONFIG_FLAG(ped,32,!seatbelt);
        lastResult=79;
    }
    if(command==80) {
        NX_SET_PED_TO_RAGDOLL(ped,4000,4000,0,false,false,false);
        lastResult=80;
    }
    if(command==81) {
        spawnOffset.x=2.0f; spawnOffset.y=0.0f; spawnOffset.z=0.0f;
        tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(ped,spawnOffset);
        spawnOffset.x=0.0f; spawnOffset.y=7.0f; spawnOffset.z=0.5f;
        float h=GET_ENTITY_HEADING(ped);
        deleteLastBodyguard();
        lastBodyguard=NX_CLONE_PED(ped,h,false,false);
        if(lastBodyguard && DOES_ENTITY_EXIST(lastBodyguard)) {
            NX_SET_ENTITY_COORDS(lastBodyguard,tempPos.x,tempPos.y,tempPos.z,false,false,false,true);
            int grp=NX_GET_PLAYER_GROUP(PLAYER_ID());
            NX_SET_PED_AS_GROUP_MEMBER(lastBodyguard,grp);
            SET_ENTITY_INVINCIBLE(lastBodyguard,true);
            NX_GIVE_WEAPON_TO_PED(lastBodyguard,0x83BF0278,9999,false,true);
            lastResult=81;
        } else lastResult=-4;
    }
    if(command==82) {
        if(lastBodyguard) {
            deleteLastBodyguard();
            lastResult=82;
        } else lastResult=-4;
    }
    if(command==83) {
        NX_STAT_SET_INT(0x0324C31D,2000000000,true);
        NX_STAT_SET_INT(0x44BD6982,2000000000,true);
        NX_STAT_SET_INT(0x8D75047D,2000000000,true);
        lastResult=83;
    }
    if(command==84) {
        Entity hostEnt=v?v:ped;
        Hash rampModel=0xB157C9E4;
        if(loadModelSync(rampModel)) {
            spawnOffset.x=0.0f; spawnOffset.y=14.0f; spawnOffset.z=-0.2f;
            tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(hostEnt,spawnOffset);
            spawnOffset.x=0.0f; spawnOffset.y=7.0f; spawnOffset.z=0.5f;
            float h=GET_ENTITY_HEADING(hostEnt);
            deleteLastObject();
            lastObject=NX_CREATE_OBJECT(rampModel,tempPos.x,tempPos.y,tempPos.z,false,false,false);
            if(lastObject && DOES_ENTITY_EXIST(lastObject)) {
                NX_SET_ENTITY_HEADING(lastObject,h);
                NX_FREEZE_ENTITY_POSITION(lastObject,true);
            }
            SET_MODEL_AS_NO_LONGER_NEEDED(rampModel);
            lastResult=84;
        } else lastResult=-3;
    }
    if(command==90) {
        toggleFlag(FLAG_RIOTMODE, argument);
        NX_SET_RIOT_MODE_ENABLED((extraFlags&FLAG_RIOTMODE)!=0);
        lastResult=90;
    }
    if(command==93) {
        SET_PLAYER_WANTED_LEVEL(PLAYER_ID(),5,false);
        SET_PLAYER_WANTED_LEVEL_NOW(PLAYER_ID(),false);
        lastResult=93;
    }
    if(command==95) {
        float h=GET_ENTITY_HEADING(v)+180.0f;
        if(h>=360.0f)h-=360.0f;
        NX_SET_ENTITY_ROTATION(v,0.0f,0.0f,h,2,true);
        lastResult=95;
    }
    int flagMask=0;
    if(command==85)flagMask=FLAG_RAINBOW;
    else if(command==86)flagMask=FLAG_AUTOREPAIR;
    else if(command==87)flagMask=FLAG_HORNBOOST;
    else if(command==88)flagMask=FLAG_VEHWEAPONS;
    else if(command==89)flagMask=FLAG_TELEGUN;
    else if(command==91)flagMask=FLAG_VEHFLY;
    else if(command==92)flagMask=FLAG_EXPLOSIONGUN;
    else if(command==94)flagMask=FLAG_VEH_INV;
    else if(command==96)flagMask=FLAG_FORCEFIELD;
    else if(command==97)flagMask=FLAG_BULLETTIME;
    else if(command==100)flagMask=FLAG_DRUNK;
    else if(command==101)flagMask=FLAG_AUTOPILOT;
    else if(command==102)flagMask=FLAG_SIREN;
    if(flagMask) {
        toggleFlag(flagMask,argument);
        if(command==94 && v)NX_SET_ENTITY_VISIBLE(v,!(extraFlags&FLAG_VEH_INV),0);
        if(command==97 && !(extraFlags&FLAG_BULLETTIME))NX_SET_TIME_SCALE(1.0f);
        if(command==100)NX_SET_PED_IS_DRUNK(ped,(extraFlags&FLAG_DRUNK)!=0);
        if(command==101) {
            if(extraFlags&FLAG_AUTOPILOT)NX_TASK_VEHICLE_DRIVE_WANDER(ped,v,30.0f,786603);
            else NX_CLEAR_PED_TASKS(ped);
        }
        if(command==102)NX_SET_VEHICLE_SIREN(v,(extraFlags&FLAG_SIREN)!=0);
        lastResult=command;
    }
    if(command==98) {
        Entity hostEnt=v?v:ped;
        NX_APPLY_FORCE_TO_ENTITY(hostEnt,1,0.0f,0.0f,60.0f,0.0f,0.0f,0.0f,0,true,true,true,false,true);
        lastResult=98;
    }
    if(command==99) {
        tempPos=GET_ENTITY_COORDS(ped,true);
        Vehicle nv=NX_GET_CLOSEST_VEHICLE(tempPos.x,tempPos.y,tempPos.z,100.0f,0,70);
        if(nv && DOES_ENTITY_EXIST(nv)) {
            NX_SET_PED_INTO_VEHICLE(ped,nv,-1);
            lastResult=99;
        } else lastResult=-5;
    }
    if(command==103) {
        Entity targetVeh=v?v:lastVehicle;
        if(targetVeh && DOES_ENTITY_EXIST(targetVeh)) {
            tempPos=GET_ENTITY_COORDS(targetVeh,true);
            NX_ADD_EXPLOSION(tempPos.x,tempPos.y,tempPos.z,0,10.0f,true,false,2.0f);
            lastResult=103;
        } else lastResult=-5;
    }
}

void beginLine(bool highlight) {
    SET_TEXT_FONT(0);SET_TEXT_SCALE(0.0f,0.38f);
    if(highlight)SET_TEXT_COLOUR(markedColor);else SET_TEXT_COLOUR(normalColor);
    SET_TEXT_OUTLINE();BEGIN_TEXT_COMMAND_DISPLAY_TEXT("STRING");
}

void endRow(int row) {
    NX_END_TEXT(0.035f,0.12f+row*0.032f,0);
}

void menuTitle(const char* name) {
    beginLine(true);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME("Menyoo | ");
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(name);
    NX_END_TEXT(0.035f,0.12f,0);
}

void mLine(const char* text) {
    beginLine(selected==menuRow);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(text);
    endRow(menuRow+2);
    menuRow++;
}

void mSub(const char* name) {
    beginLine(selected==menuRow);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(name);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(" >");
    endRow(menuRow+2);
    menuRow++;
}

void mToggle(const char* prefix,bool state) {
    beginLine(selected==menuRow);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(prefix);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(state?"ON":"OFF");
    endRow(menuRow+2);
    menuRow++;
}

void mChoice(const char* prefix,const char* val) {
    beginLine(selected==menuRow);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(prefix);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME("< ");
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(val);
    ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(" >");
    endRow(menuRow+2);
    menuRow++;
}

void drawMenu() {
    menuRow=0;
    if(currentMenu==0) {
        menuTitle("Main");
        mSub("Player");
        mSub("Vehicle");
        mSub("Spawner");
        mSub("Teleport");
        mSub("Weapons");
        mSub("World");
        mSub("Customs");
        mSub("Appearance");
        mSub("Animations");
        mSub("Spooner");
        mSub("Settings");
        mLine("Close Menu");
    } else if(currentMenu==1) {
        menuTitle("Player");
        mLine("< Back");
        mLine("Heal + Armour");
        mLine("Clear Wanted");
        mToggle("Invincible: ",invincible);
        mToggle("Never Wanted: ",neverWanted);
        mToggle("Super Jump: ",superJump);
        mToggle("Fast Sprint: ",fastSprint);
        mToggle("Fast Swim: ",fastSwim);
        mToggle("Never Tired: ",neverTired);
        mToggle("Police Ignore: ",ignoredByCops);
        mToggle("Thermal Vision: ",thermalVision);
        mToggle("Night Vision: ",nightVision);
        mLine("Clean Clothes");
        mToggle("Invisible: ",invisible);
        mToggle("No Ragdoll: ",noRagdoll);
        mLine("Suicide");
        mToggle("Seatbelt: ",seatbelt);
        mLine("Ragdoll Now");
        mLine("Max Cash ($2B)");
        mLine("Spawn Bodyguard");
        mLine("Dismiss Guard");
        mLine("5-Star Wanted");
        mToggle("Forcefield: ",(extraFlags&FLAG_FORCEFIELD)!=0);
        mLine("Sky Launch");
        mToggle("Drunk Mode: ",(extraFlags&FLAG_DRUNK)!=0);
    } else if(currentMenu==2) {
        menuTitle("Vehicle");
        mLine("< Back");
        mLine("Repair Vehicle");
        mLine("Clean Vehicle");
        mLine("Fix Tyres");
        mLine("Flip Upright");
        mLine("Max Tuning");
        mToggle("Engine On: ",engineAlwaysOn);
        mToggle("Veh Godmode: ",vehGodmode);
        mLine("Bulletproof Tyres");
        mLine("Stop Vehicle");
        mLine("Speed Boost");
        mLine("Toggle Doors");
        mChoice("Respray: ",getColorName(colorIndex));
        mChoice("Plate: ",getPlateName(plateIndex));
        mLine("Delete Spawned");
        mLine("Vehicle Jump");
        mToggle("Drift Mode: ",driftMode);
        mLine("Rocket Boost");
        mLine("Stunt Ramp Ahead");
        mToggle("Auto Repair: ",(extraFlags&FLAG_AUTOREPAIR)!=0);
        mToggle("Horn Boost: ",(extraFlags&FLAG_HORNBOOST)!=0);
        mToggle("Veh Weapons: ",(extraFlags&FLAG_VEHWEAPONS)!=0);
        mToggle("Flying Car: ",(extraFlags&FLAG_VEHFLY)!=0);
        mLine("Instant 180");
        mToggle("Invisible Veh: ",(extraFlags&FLAG_VEH_INV)!=0);
        mToggle("Autopilot: ",(extraFlags&FLAG_AUTOPILOT)!=0);
        mToggle("Siren: ",(extraFlags&FLAG_SIREN)!=0);
        mLine("Self-Destruct");
    } else if(currentMenu==3) {
        menuTitle("Spawner");
        mLine("< Back");
        mChoice("Category: ",getCategoryName(categoryIndex));
        mChoice("Model: ",getModelName(categoryIndex,categoryModelIndex));
        mLine("Spawn Vehicle");
        mToggle("Spawn Inside: ",spawnInVehicle);
        mToggle("Spawn Tuned: ",spawnTuned);
        mToggle("Spawn Godmode: ",spawnGodmode);
        mLine("Delete Spawned");
    } else if(currentMenu==4) {
        menuTitle("Teleport");
        mLine("< Back");
        mLine("Waypoint");
        mLine("Forward 5m");
        mLine("Michael");
        mLine("Franklin");
        mLine("Trevor");
        mLine("LS Customs");
        mLine("LSIA Airport");
        mLine("Maze Bank");
        mLine("Mount Chiliad");
        mLine("Fort Zancudo");
        mLine("Prison");
        mLine("Observatory");
        mLine("Sandy Shores");
        mLine("Paleto Bay");
        mLine("Del Perro Pier");
        mLine("Nearest Vehicle");
    } else if(currentMenu==5) {
        menuTitle("Weapons");
        mLine("< Back");
        mLine("Give All");
        mLine("Max Ammo");
        mToggle("Infinite Ammo: ",infiniteAmmo);
        mToggle("Never Reload: ",neverReload);
        mToggle("Explosive Ammo: ",explosiveAmmo);
        mToggle("Fire Ammo: ",fireAmmo);
        mToggle("Explosive Melee: ",explosiveMelee);
        mToggle("Super Damage: ",superDamage);
        mLine("Give Heavy");
        mLine("Parachute");
        mLine("Remove All");
        mLine("Air Strike Ahead");
        mToggle("Teleport Gun: ",(extraFlags&FLAG_TELEGUN)!=0);
        mToggle("Explosion Gun: ",(extraFlags&FLAG_EXPLOSIONGUN)!=0);
    } else if(currentMenu==6) {
        menuTitle("World");
        mLine("< Back");
        mToggle("Pause Clock: ",clockPaused);
        mChoice("Time: ",getTimePresetName(timePresetIndex));
        mLine("Apply Time");
        mChoice("Weather: ",getWeatherPresetDisplayName(weatherPresetIndex));
        mLine("Apply Weather");
        mLine("Reset Weather");
        mToggle("Low Gravity: ",lowGravity);
        mLine("Clear Peds");
        mLine("Clear Vehicles");
        mLine("Clear Cops");
        mToggle("Blackout: ",blackout);
        mChoice("Speed: ",getSpeedName(gameSpeedIndex));
        mToggle("Riot Mode: ",(extraFlags&FLAG_RIOTMODE)!=0);
        mToggle("Aim Slowmo: ",(extraFlags&FLAG_BULLETTIME)!=0);
    } else if(currentMenu==7) {
        menuTitle("Customs");
        mLine("< Back");
        mToggle("Neons: ",neonsOn);
        mChoice("Neon Colour: ",getNeonColorName(neonColorIndex));
        mLine("Cycle Extra");
        mChoice("Window Tint: ",getWindowTintName(tintIndex));
        mChoice("Wheel Type: ",getWheelTypeName(wheelTypeIndex));
        mChoice("Custom Paint: ",getCustomPaintName(customPaintIndex));
        mLine("Clean Vehicle");
        mToggle("Rainbow Paint: ",(extraFlags&FLAG_RAINBOW)!=0);
    } else if(currentMenu==8) {
        menuTitle("Appearance");
        mLine("< Back");
        mLine("Model: Michael");
        mLine("Model: Franklin");
        mLine("Model: Trevor");
        mLine("Model: MP Male");
        mLine("Model: MP Female");
        mLine("Reset Outfit");
        mLine("Cycle Torso");
        mLine("Cycle Legs");
    } else if(currentMenu==9) {
        menuTitle("Animations");
        mLine("< Back");
        mLine("Smoke");
        mLine("Drink Coffee");
        mLine("Cheer");
        mLine("Flex Muscles");
        mLine("Binoculars");
        mLine("Push-ups");
        mLine("Sit-ups");
        mLine("Guard Stand");
        mLine("Stop Animation");
    } else if(currentMenu==10) {
        menuTitle("Spooner");
        mLine("< Back");
        mLine("Spawn Cone");
        mLine("Spawn Barrier");
        mLine("Spawn Ramp");
        mLine("Spawn Box");
        mLine("Attach to Player");
        mToggle("Freeze: ",objFrozen);
        mLine("Delete Spawned");
    } else if(currentMenu==11) {
        menuTitle("Settings");
        mLine("< Back");
        mToggle("Spawn Inside: ",spawnInVehicle);
        mToggle("Spawn Tuned: ",spawnTuned);
        mToggle("Spawn Godmode: ",spawnGodmode);
        mLine("Stop Trainer");
    }

    const char* st=0;
    if(lastResult==1)st="Loading...";
    else if(lastResult==12)st="Locating ground...";
    else if(lastResult>0)st="Done";
    else if(lastResult==-5)st="Need Vehicle";
    else if(lastResult==-12)st="No Waypoint";
    else if(lastResult==-13)st="Ground timeout";
    else if(lastResult<0)st="Error";
    if(st) {
        beginLine(lastResult>0);
        ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(st);
        endRow(18);
    }
}

void main() {
    /* Reading these globals keeps the ABI identifiers in compiler output. */
    if(protocolMagic!=0x4e585431 || protocolVersion!=1)return;
    runtimeStatus=1;
    while(true) {
        WAIT(0);heartbeat++;
        if(runtimeStatus==2) {WAIT(1000);continue;}
        Ped ped=PLAYER_PED_ID();
        if(ped!=previousPed) {
            if(invincible && previousPed && DOES_ENTITY_EXIST(previousPed)) {
                SET_ENTITY_INVINCIBLE(previousPed,false);
            }
            previousPed=ped;
            if(invincible && DOES_ENTITY_EXIST(ped) && !IS_ENTITY_DEAD(ped)) {
                SET_ENTITY_INVINCIBLE(ped,true);
            }
            releasePending();
            if(teleportState!=0)teleportState=0;
        }
        if(remoteCommand) {
            int command=remoteCommand;
            int argument=remoteArg;
            remoteCommand=0;
            action(command,argument);
            acknowledgedSequence=remoteSequence;
        }
        if(runtimeStatus==2)continue;
        if(!DOES_ENTITY_EXIST(ped) || IS_ENTITY_DEAD(ped)) {
            if(teleportState!=0)teleportState=0;
            releasePending();
            continue;
        }

        /* Continuous per-frame feature updates */
        if(neverWanted) {
            SET_PLAYER_WANTED_LEVEL(PLAYER_ID(),0,false);
            SET_PLAYER_WANTED_LEVEL_NOW(PLAYER_ID(),false);
        }
        if(superJump)NX_SET_SUPER_JUMP_THIS_FRAME(PLAYER_ID());
        if(neverTired)NX_RESTORE_PLAYER_STAMINA(PLAYER_ID(),1.0f);
        if(explosiveAmmo)NX_SET_EXPLOSIVE_AMMO_THIS_FRAME(PLAYER_ID());
        if(fireAmmo)NX_SET_FIRE_AMMO_THIS_FRAME(PLAYER_ID());
        if(explosiveMelee)NX_SET_EXPLOSIVE_MELEE_THIS_FRAME(PLAYER_ID());
        if(infiniteAmmo) {
            NX_SET_PED_INFINITE_AMMO(ped,true,0);
            NX_SET_PED_INFINITE_AMMO_CLIP(ped,neverReload);
        }
        if(IS_PED_IN_ANY_VEHICLE(ped,false)) {
            Vehicle curVeh=GET_VEHICLE_PED_IS_IN(ped,false);
            if(vehGodmode) {
                SET_ENTITY_INVINCIBLE(curVeh,true);
                NX_SET_VEHICLE_CAN_BE_VISIBLY_DAMAGED(curVeh,false);
                NX_SET_VEHICLE_TYRES_CAN_BURST(curVeh,false);
            }
            if(engineAlwaysOn) {
                NX_SET_VEHICLE_ENGINE_ON(curVeh,true,true,false);
            }
            if(driftMode) {
                NX_SET_VEHICLE_REDUCE_GRIP(curVeh,true);
            }
        }
        if(seatbelt) {
            NX_SET_PED_CONFIG_FLAG(ped,32,false);
        }
        if((extraFlags&FLAG_TELEGUN)&&IS_PED_SHOOTING(ped)) {
            if(NX_GET_PED_LAST_WEAPON_IMPACT_COORD(ped,&tempPos)) {
                NX_SET_ENTITY_COORDS(ped,tempPos.x,tempPos.y,tempPos.z+1.0f,false,false,false,true);
            }
        }
        if((extraFlags&FLAG_EXPLOSIONGUN)&&IS_PED_SHOOTING(ped)) {
            if(NX_GET_PED_LAST_WEAPON_IMPACT_COORD(ped,&tempPos)) {
                NX_ADD_EXPLOSION(tempPos.x,tempPos.y,tempPos.z,29,5.0f,true,false,1.0f);
            }
        }
        if(extraFlags&FLAG_FORCEFIELD) {
            tempPos=GET_ENTITY_COORDS(ped,true);
            NX_ADD_EXPLOSION(tempPos.x,tempPos.y,tempPos.z,70,0.0f,false,true,0.0f);
        }
        if(extraFlags&FLAG_BULLETTIME) {
            if(IS_CONTROL_PRESSED(0,25))NX_SET_TIME_SCALE(0.2f);
            else NX_SET_TIME_SCALE(1.0f);
        }
        if(IS_PED_IN_ANY_VEHICLE(ped,false)) {
            Vehicle actVeh=GET_VEHICLE_PED_IS_IN(ped,false);
            if(extraFlags&FLAG_AUTOREPAIR) {
                SET_VEHICLE_FIXED(actVeh);
                NX_SET_VEHICLE_DEFORMATION_FIXED(actVeh);
                NX_SET_VEHICLE_DIRT_LEVEL(actVeh,0.0f);
            }
            if(extraFlags&FLAG_RAINBOW) {
                rainbowStep++;
                applyRainbowColor(actVeh,rainbowStep);
            }
            if((extraFlags&FLAG_HORNBOOST)&&IS_CONTROL_JUST_PRESSED(0,86)) {
                NX_SET_VEHICLE_FORWARD_SPEED(actVeh,50.0f);
            }
            if((extraFlags&FLAG_VEHFLY)&&IS_CONTROL_PRESSED(0,76)) {
                NX_APPLY_FORCE_TO_ENTITY(actVeh,1,0.0f,15.0f,8.0f,0.0f,0.0f,0.0f,0,true,true,true,false,true);
            }
            if((extraFlags&FLAG_VEHWEAPONS)&&(IS_CONTROL_JUST_PRESSED(0,69)||IS_CONTROL_JUST_PRESSED(0,86))) {
                spawnOffset.x=0.0f; spawnOffset.y=3.0f; spawnOffset.z=0.5f;
                tempPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(actVeh,spawnOffset);
                spawnOffset.x=0.0f; spawnOffset.y=80.0f; spawnOffset.z=0.5f;
                vector3 targetPos=GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(actVeh,spawnOffset);
                spawnOffset.x=0.0f; spawnOffset.y=7.0f; spawnOffset.z=0.5f;
                NX_SHOOT_SINGLE_BULLET(tempPos.x,tempPos.y,tempPos.z,targetPos.x,targetPos.y,targetPos.z,250,true,0x7F7497E5,ped,true,false,300.0f);
            }
        }

        updateVehicle(ped);
        updateTeleport(ped);

        /* Shortcut: Cover (44 / RB) + D-pad Left (189) or Right (38) */
        if(IS_CONTROL_PRESSED(0,44) && (IS_CONTROL_JUST_PRESSED(2,189) || IS_CONTROL_JUST_PRESSED(0,38))) {
            menuOpen=!menuOpen;
        }

        /* Never consume frontend controls during game pause, loading, or screen fade */
        if(NX_IS_PAUSE_MENU_ACTIVE() || NX_IS_SCREEN_FADED_OUT() || NX_IS_SCREEN_FADING_OUT()) {
            continue;
        }
        if(!menuOpen)continue;

        /* Disable frontend controls while menu is active */
        for(int c=187;c<=190;c++)DISABLE_CONTROL_ACTION(2,c,true);
        DISABLE_CONTROL_ACTION(2,201,true);
        DISABLE_CONTROL_ACTION(2,202,true);

        /* Delayed key repeat for D-pad navigation */
        bool upPressed=false;
        bool downPressed=false;
        bool leftPressed=false;
        bool rightPressed=false;
        int now=GET_GAME_TIMER();

        if(IS_DISABLED_CONTROL_JUST_PRESSED(2,188)) {
            upPressed=true;repeatControl=188;repeatTimer=now+350;
        } else if(repeatControl==188&&now>repeatTimer&&NX_IS_DISABLED_CONTROL_PRESSED(2,188)) {
            upPressed=true;repeatTimer=now+140;
        }

        if(IS_DISABLED_CONTROL_JUST_PRESSED(2,187)) {
            downPressed=true;repeatControl=187;repeatTimer=now+350;
        } else if(repeatControl==187&&now>repeatTimer&&NX_IS_DISABLED_CONTROL_PRESSED(2,187)) {
            downPressed=true;repeatTimer=now+140;
        }

        if(IS_DISABLED_CONTROL_JUST_PRESSED(2,189)) {
            leftPressed=true;repeatControl=189;repeatTimer=now+350;
        } else if(repeatControl==189&&now>repeatTimer&&NX_IS_DISABLED_CONTROL_PRESSED(2,189)) {
            leftPressed=true;repeatTimer=now+140;
        }

        if(IS_DISABLED_CONTROL_JUST_PRESSED(2,190)) {
            rightPressed=true;repeatControl=190;repeatTimer=now+350;
        } else if(repeatControl==190&&now>repeatTimer&&NX_IS_DISABLED_CONTROL_PRESSED(2,190)) {
            rightPressed=true;repeatTimer=now+140;
        }

        if(repeatControl&&!NX_IS_DISABLED_CONTROL_PRESSED(2,repeatControl)) {
            repeatControl=0;
        }

        int maxR=getMaxRows(currentMenu);
        if(upPressed)selected=(selected+maxR-1)%maxR;
        if(downPressed)selected=(selected+1)%maxR;

        /* Left / Right horizontal adjustment */
        bool horiz=leftPressed||rightPressed;
        if(horiz) {
            if(currentMenu==1) {
                if(selected==16||selected==22||selected==24)action(selected==16?79:(selected==22?96:100),2);
            } else if(currentMenu==2) {
                if(selected==12) {
                    if(leftPressed)colorIndex=(colorIndex+7)%8; else colorIndex=(colorIndex+1)%8;
                    action(31,colorIndex);
                } else if(selected==13) {
                    if(leftPressed)plateIndex=(plateIndex+3)%4; else plateIndex=(plateIndex+1)%4;
                    action(32,plateIndex);
                } else if(selected==16)action(76,2);
                else if(selected>=19&&selected<=22)action(selected==22?91:(67+selected),2);
                else if(selected==24)action(94,2);
                else if(selected>=25&&selected<=26)action(selected==25?101:102,2);
            } else if(currentMenu==3) {
                if(selected==1) {
                    if(leftPressed)categoryIndex=(categoryIndex+6)%7; else categoryIndex=(categoryIndex+1)%7;
                    categoryModelIndex=0;
                } else if(selected==2) {
                    int count=getCategoryModelCount(categoryIndex);
                    if(leftPressed)categoryModelIndex=(categoryModelIndex+count-1)%count;
                    else categoryModelIndex=(categoryModelIndex+1)%count;
                } else if(selected==4)spawnInVehicle=!spawnInVehicle;
                else if(selected==5)spawnTuned=!spawnTuned;
                else if(selected==6)spawnGodmode=!spawnGodmode;
            } else if(currentMenu==5) {
                if(selected==13||selected==14)action(selected==13?89:92,2);
            } else if(currentMenu==6) {
                if(selected==1) {clockPaused=!clockPaused;action(17,clockPaused);}
                else if(selected==2) {
                    if(leftPressed)timePresetIndex=(timePresetIndex+3)%4; else timePresetIndex=(timePresetIndex+1)%4;
                } else if(selected==4) {
                    if(leftPressed)weatherPresetIndex=(weatherPresetIndex+6)%7; else weatherPresetIndex=(weatherPresetIndex+1)%7;
                } else if(selected==11) {blackout=!blackout;action(39,blackout);}
                else if(selected==12) {
                    if(leftPressed)gameSpeedIndex=(gameSpeedIndex+2)%3; else gameSpeedIndex=(gameSpeedIndex+1)%3;
                    action(40,gameSpeedIndex);
                } else if(selected==13)action(90,2);
                else if(selected==14)action(97,2);
            } else if(currentMenu==7) {
                if(selected==1||selected==8)action(selected==1?60:85,2);
                else if(selected==2) {
                    if(leftPressed)neonColorIndex=(neonColorIndex+7)%8; else neonColorIndex=(neonColorIndex+1)%8;
                    action(61,neonColorIndex);
                } else if(selected==4) {
                    if(leftPressed)tintIndex=(tintIndex+5)%6; else tintIndex=(tintIndex+1)%6;
                    action(63,tintIndex);
                } else if(selected==5) {
                    if(leftPressed)wheelTypeIndex=(wheelTypeIndex+6)%7; else wheelTypeIndex=(wheelTypeIndex+1)%7;
                    action(64,wheelTypeIndex);
                } else if(selected==6) {
                    if(leftPressed)customPaintIndex=(customPaintIndex+4)%5; else customPaintIndex=(customPaintIndex+1)%5;
                    action(65,customPaintIndex);
                }
            } else if(currentMenu==10) {
                if(selected==6)action(73,2);
            } else if(currentMenu==11) {
                if(selected==1)spawnInVehicle=!spawnInVehicle;
                else if(selected==2)spawnTuned=!spawnTuned;
                else if(selected==3)spawnGodmode=!spawnGodmode;
            }
        }

        /* Cancel (B button): Back or Close */
        bool cancelPressed = IS_DISABLED_CONTROL_JUST_PRESSED(2,202) || IS_CONTROL_JUST_PRESSED(2,202) ||
                             IS_DISABLED_CONTROL_JUST_PRESSED(2,194) || IS_CONTROL_JUST_PRESSED(2,194) ||
                             IS_DISABLED_CONTROL_JUST_PRESSED(0,202) || IS_CONTROL_JUST_PRESSED(0,202);
        if(cancelPressed) {
            if(teleportState!=0) {
                teleportState=0;
                lastResult=0;
            } else if(currentMenu!=0) {
                selected=currentMenu-1;
                currentMenu=0;
            } else {
                menuOpen=false;
            }
            continue;
        }

        drawMenu();

        /* Accept (A button) */
        bool acceptPressed = IS_DISABLED_CONTROL_JUST_PRESSED(2,201) || IS_CONTROL_JUST_PRESSED(2,201) ||
                             IS_DISABLED_CONTROL_JUST_PRESSED(0,201) || IS_CONTROL_JUST_PRESSED(0,201);
        if(!acceptPressed)continue;

        if(currentMenu!=0&&selected==0) {
            /* Back option */
            selected=currentMenu-1;
            currentMenu=0;
            continue;
        }

        if(currentMenu==0) {
            if(selected<11) {
                currentMenu=selected+1;
                selected=0;
            } else {
                menuOpen=false;
            }
        } else if(currentMenu==1) { // Player
            if(selected==1)action(3,0); // Heal
            else if(selected==2)action(4,0); // Clear Wanted
            else if(selected>=3&&selected<=6)action(selected==3?6:(selected+16),2); // 3->6, 4->20, 5->22, 6->23
            else if(selected>=7&&selected<=11)action(selected+34,2); // 7..11 -> 41..45
            else if(selected==12)action(24,0); // Clean Clothes
            else if(selected==13||selected==14)action(selected+12,2); // 13->25, 14->26
            else if(selected==15)action(27,0); // Suicide
            else if(selected==16)action(79,2); // Seatbelt
            else if(selected==17)action(80,0); // Ragdoll
            else if(selected==18)action(83,0); // Max Cash
            else if(selected==19||selected==20)action(selected+62,0); // 19->81, 20->82
            else if(selected==21)action(93,0); // 5-Star Wanted
            else if(selected==22)action(96,2); // Forcefield
            else if(selected==23)action(98,0); // Sky Launch
            else if(selected==24)action(100,2); // Drunk Mode
        } else if(currentMenu==2) { // Vehicle
            if(selected==1)action(5,0); // Repair
            else if(selected==2)action(10,0); // Clean
            else if(selected==3)action(46,0); // Fix tyres
            else if(selected==4||selected==5)action(selected+7,0); // 4->11, 5->12
            else if(selected==6)action(47,2);
            else if(selected==7)action(28,2);
            else if(selected==8||selected==9)action(selected+40,0); // 8->48, 9->49
            else if(selected==10||selected==11)action(selected+19,0); // 10->29, 11->30
            else if(selected==12)action(31,colorIndex);
            else if(selected==13)action(32,plateIndex);
            else if(selected==14)action(13,0); // Delete
            else if(selected==15||selected==17)action(selected+60,0); // 15->75, 17->77
            else if(selected==16)action(76,2); // Drift Mode
            else if(selected==18)action(84,0); // Stunt Ramp Ahead
            else if(selected>=19&&selected<=22)action(selected==22?91:(67+selected),2);
            else if(selected==23)action(95,0); // Instant 180
            else if(selected==24)action(94,2); // Invisible Veh
            else if(selected==25||selected==26)action(selected+76,2); // 25->101, 26->102
            else if(selected==27)action(103,0); // Self-Destruct
        } else if(currentMenu==3) { // Spawner
            if(selected==1||selected==2||selected==3) {
                action(2,GET_HASH_KEY(getModelName(categoryIndex,categoryModelIndex)));
            } else if(selected==4) {
                spawnInVehicle=!spawnInVehicle;
            } else if(selected==5) {
                spawnTuned=!spawnTuned;
            } else if(selected==6) {
                spawnGodmode=!spawnGodmode;
            } else if(selected==7) {
                action(13,0);
            }
        } else if(currentMenu==4) { // Teleport
            if(selected==1)action(15,0); // Waypoint
            else if(selected==2)action(50,5); // Forward 5m
            else if(selected>=3&&selected<=15)action(14,selected-3);
            else if(selected==16)action(99,0); // Nearest Vehicle
        } else if(currentMenu==5) { // Weapons
            if(selected>=1&&selected<=4)action(selected+32,selected<=2?0:2);
            else if(selected>=5&&selected<=8)action(selected+46,2);
            else if(selected==9)action(55,0); // Give Heavy
            else if(selected==10||selected==11)action(selected+27,0);
            else if(selected==12)action(78,0); // Air Strike
            else if(selected==13||selected==14)action(selected==13?89:92,2);
        } else if(currentMenu==6) { // World
            if(selected==1) {clockPaused=!clockPaused;action(17,clockPaused);}
            else if(selected==2||selected==3)action(16,getTimePresetHour(timePresetIndex));
            else if(selected==4||selected==5)action(18,weatherPresetIndex);
            else if(selected==6)action(19,0);
            else if(selected==7)action(56,2);
            else if(selected>=8&&selected<=10)action(selected+49,0);
            else if(selected==11)action(39,2);
            else if(selected==12)action(40,gameSpeedIndex);
            else if(selected==13||selected==14)action(selected==13?90:97,2);
        } else if(currentMenu==7) { // Customs
            if(selected==1)action(60,2);
            else if(selected==2)action(61,neonColorIndex);
            else if(selected==3)action(62,0);
            else if(selected==4)action(63,tintIndex);
            else if(selected==5)action(64,wheelTypeIndex);
            else if(selected==6)action(65,customPaintIndex);
            else if(selected==7)action(10,0); // Clean
            else if(selected==8)action(85,2); // Rainbow Paint
        } else if(currentMenu==8) { // Appearance
            if(selected>=1&&selected<=5)action(66,selected-1);
            else if(selected==6)action(67,0); // Reset Outfit
            else if(selected>=7&&selected<=8)action(68,selected-4);
        } else if(currentMenu==9) { // Animations
            if(selected>=1 && selected<=8)action(69,selected-1);
            else if(selected==9)action(70,0); // Stop
        } else if(currentMenu==10) { // Spooner
            if(selected>=1 && selected<=4)action(71,selected-1);
            else if(selected==5)action(72,0); // Attach
            else if(selected==6)action(73,2); // Freeze
            else if(selected==7)action(74,0); // Delete
        } else if(currentMenu==11) { // Settings
            if(selected==1)spawnInVehicle=!spawnInVehicle;
            else if(selected==2)spawnTuned=!spawnTuned;
            else if(selected==3)spawnGodmode=!spawnGodmode;
            else if(selected==4)cleanup();
        }
    }
}
