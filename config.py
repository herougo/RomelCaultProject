
#TRIPS_FOLDER = 'D:\\Desktop\\Work\\IMS Work\\Car vs Bus\\Trips\\Bus'
#TRIPS_FOLDER = 'D:\\Desktop\\Work\\IMS Work\\Car vs Bus\\Data Normalization\\SensorCalibrationDataSet\\+45'
#TRIPS_NAME = 'Wed Jan 21 12%3A39%3A59 2015.csv'
#TRIPS_NAME = 'AA0000000004408_1444048494791_Bus.csv'
#TRIPS_NAME = 'AA0000000004406_1443105972728_Bus.csv'
TRIPS_NAME = 'raw001.csv'

#Rotation Strings
RS_PHI = '1 0 0; 0 {0} {1}; 0 {2} {3}'    
RS_THETA = '{0} 0 {1}; 0 1 0; {2} 0 {3}'    
RS_PSI = '{0} {1} 0; {2} {3} 0; 0 0 1' 

#Rotation Angels
TCN_PHI = 'phi'
TCN_THETA = 'theta'
TCN_PSI = 'psi'

#Sensor Sample Rates
SSR_ACCEL = 10
SSR_GYRO = 10
SSR_MAG_HEADING = 10
SSR_GRAV = 10
SSR_GPS = 1
SSR_USER_ACCEL = 10
SSR_EULER_ANGLE = 10
SSR_TIME_SYNC = 10

#Stability Detection
SD_WINDOW = 5*SSR_ACCEL
SD_MAX_GYRO_POWER = 0.02

#Trip Codes
TC_START = 240
TC_STOP = 241
TC_GPS = 131
#TC_ACCELEROMETER = 127
TC_ACCELEROMETER = 128
TC_USER_ACCELEROMETER = 129
#TC_USER_ACCELEROMETER = 126
TC_GYROSCOPE = 166
#TC_GYROSCOPE = 167
TC_PHONE_INFO = 800
TC_GRAVITY = 125
TC_MAG_HEADING = 152
TC_EULER_ANGLE = 160
TC_FUSION = 999
TC_TIME_SYNC = 998

#columns names
TCN_CODE = 'code'
TCN_TIME = 'time'
TCN_COL2 = 'c2'
TCN_COL3 = 'c3'
TCN_COL4 = 'c4'
TCN_COL5 = 'c5'
TCN_COL6 = 'c6'
TCN_COL7 = 'c7'
TCN_COL8 = 'c8'
TCN_COL9 = 'c9'
TCN_COL10 = 'c10'
TCN_GPS_LAT = 'latitude'
TCN_GPS_LON = 'longitude'
TCN_GPS_HEADING = 'heading'
TCN_GPS_SPEED = 'speed'
TCN_ACCEL_X = 'accel_x' 
TCN_ACCEL_Y = 'accel_y'
TCN_ACCEL_Z = 'accel_z'
TCN_USER_ACCEL_X = 'user_accel_x' 
TCN_USER_ACCEL_Y = 'user_accel_y'
TCN_USER_ACCEL_Z = 'user_accel_z'
TCN_GYRO_PITCH = 'pitch'
TCN_GYRO_ROLL = 'roll'
TCN_GYRO_YAW = 'yaw'
TCN_GRAV_X = 'gravity_x'
TCN_GRAV_Y = 'gravity_y'
TCN_GRAV_Z = 'gravity_z' 
TCN_MAG_HEAING_X = 'mag_heading_x'   
TCN_MAG_HEAING_Y = 'mag_heading_y'   
TCN_MAG_HEAING_Z = 'mag_heading_z'   
TCN_MAG_HEAING_DEGREES = 'mag_heading_degrees'   
TCN_MAG_HEAING_ACCURACY = 'mag_heading_accuracy'   
TCN_EULER_ANGLE_X = 'euler_angle_x'
TCN_EULER_ANGLE_Y = 'euler_angle_y'
TCN_EULER_ANGLE_Z = 'euler_angle_z'
TCN_NORM_YAW = 'norm_yaw'



T_RAW_COLUMNS = [TCN_CODE, TCN_TIME, TCN_COL2, TCN_COL3, TCN_COL4, TCN_COL5, TCN_COL6, TCN_COL7, TCN_COL8, TCN_COL9, TCN_COL10]
T_GPS_COLUMNS = [TCN_TIME, TCN_GPS_LAT, TCN_GPS_LON, TCN_GPS_HEADING, TCN_GPS_SPEED]
T_ACCEL_COLUMNS = [TCN_TIME, TCN_ACCEL_X, TCN_ACCEL_Y, TCN_ACCEL_Z]
T_GYRO_COLUMNS = [TCN_TIME, TCN_GYRO_PITCH, TCN_GYRO_ROLL, TCN_GYRO_YAW]
T_GRAV_COLUMNS = [TCN_TIME, TCN_GRAV_X, TCN_GRAV_Y, TCN_GRAV_Z]
T_MAG_HEADING_COLUMNS = [TCN_TIME, TCN_MAG_HEAING_X, TCN_MAG_HEAING_Y, TCN_MAG_HEAING_Z, TCN_MAG_HEAING_DEGREES, TCN_MAG_HEAING_ACCURACY]
T_USER_ACCEL_COLUMNS = [TCN_TIME, TCN_USER_ACCEL_X, TCN_USER_ACCEL_Y, TCN_USER_ACCEL_Z]
T_EULER_ANGLE_COLUMNS = [TCN_TIME, TCN_EULER_ANGLE_X, TCN_EULER_ANGLE_Y, TCN_EULER_ANGLE_Z]
T_FUSION_COLUMNS = [TCN_TIME, TCN_USER_ACCEL_X, TCN_USER_ACCEL_Y, TCN_USER_ACCEL_Z, TCN_GYRO_PITCH, TCN_GYRO_ROLL, TCN_GYRO_YAW, TCN_NORM_YAW]
T_TIME_SYNC_COLUMNS = [TCN_TIME, TCN_USER_ACCEL_X, TCN_USER_ACCEL_Y, TCN_USER_ACCEL_Z, TCN_GYRO_PITCH, TCN_GYRO_ROLL, TCN_GYRO_YAW, TCN_EULER_ANGLE_X, TCN_EULER_ANGLE_Y]

#time to Display
TIME_TO_DISPLAY = 2


GRAV = 'grav'
ACCEL = 'accel'
MAG_HEADING = 'mag_heading'
GPS = 'gps'
GYRO = 'gyro'
EULER_ANGLE = 'euler_angle'
USER_ACCEL = 'user_accel'
FUSION = 'fusion'
TIME_SYNC = 'time_sync'
DUMMY = 'dummy'
DUMMY2 = 'dummy2'

global datatypeDict;
datatypeDict  = {
            GRAV:['gravity_x', 'gravity_y', 'gravity_z'],
#             ACCEL:['user_accel_x', 'user_accel_y', 'user_accel_z'],
#             MAG_HEADING:['mag_heading_x', 'mag_heading_y', 'mag_heading_z', 'mag_heading_degrees', 'mag_heading_accuracy'], 
#             GPS:['latitude', 'longitude', 'heading', 'speed'],
#             GYRO:['pitch', 'roll', 'yaw'],
#             EULER_ANGLE:['euler_angle_x', 'euler_angle_y', 'euler_angle_z'],
            USER_ACCEL:['user_accel_x', 'user_accel_y', 'user_accel_z'],
#             FUSION:['user_accel_x', 'user_accel_y', 'user_accel_z', 'pitch', 'roll', 'yaw', 'norm_yaw'], 
#             TIME_SYNC:['user_accel_x', 'user_accel_y', 'user_accel_z', 'pitch', 'roll', 'yaw', 'euler_angle_x', 'euler_angle_y'],  
            DUMMY:['user_accel_x', 'user_accel_y', 'user_accel_z']
#             DUMMY2:['fake']
            }

#Phone Data Key
PDK_ACCEL = 'pdk_accel'
PDK_GRAV = 'pdk_grav'
PDK_MAG_HEADING = 'pdk_mag_heading'
PDK_GPS = 'pdk_gps'
PDK_GYRO = 'pdk_gyro'
PDK_EULER_ANGLE = 'pdk_euler_angle'
PDK_USER_ACCEL = 'pdk_user_accel'
PDK_FUSION = 'pdk_fusion'
PDK_TIME_SYNC = 'pdk_time_sync'