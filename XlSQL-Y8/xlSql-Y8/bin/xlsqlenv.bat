@echo on
rem =========
rem xlSQL_setenv
rem =========
rem Windows XP PATH
for %%x in (%0) do set CurDir=%%~dpsx
for %%x in (%CurDir%) do set CurDir=%%~dpsx
set PATH=%PATH%;%CurDir%;%CurDir%mysql\bin
rem
rem Java CLASSPATH
set CLASSPATH=%CLASSPATH%;%CurDir%..\xlSQL_Y8.jar
rem =======
rem jConfig
rem =======
set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\jconfig\jconfig.jar
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\jconfig\crimson.jar
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\jconfig\jaxp.jar
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\jmxri.jar
rem =======
rem Commons
rem =======
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\commons\commons-beanutils.jar
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\commons\commons-collections-3.1.jar
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\commons\commons-digester.jar
set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\commons\commons-logging.jar
set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\commons\commons-cli-1.0.jar
rem ==============
rem Java Excel API
rem ==============
set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\jexcelapi\jxl.jar
rem ======
rem HSQLDBD
rem ======
set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\hsqldb\hsqldb.jar
rem =====
rem MySQL
rem =====
REM set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\mysql\mysql-connector-java-3.0.10-stable-bin.jar
set CLASSPATH=%CLASSPATH%;%CurDir%..\lib\mysql\mysql-connector-java-5.1.6-bin.jar
rem ====
rem JDOM
rem ====
REM set classpath=%classpath%;p:\xlSQL\lib\jdom\jdom.jar
