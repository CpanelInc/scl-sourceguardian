OBS_PROJECT := EA4
sourceguardian81-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
sourceguardian80-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
sourceguardian74-obs : DISABLE_BUILD += repository=CentOS_6.5_standard repository=CentOS_9
sourceguardian73-obs : DISABLE_BUILD += repository=CentOS_6.5_standard repository=CentOS_9
sourceguardian72-obs : DISABLE_BUILD += repository=xUbuntu_20.04 repository=CentOS_9
sourceguardian71-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04
sourceguardian70-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04
sourceguardian56-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04
sourceguardian55-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04
sourceguardian54-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04
OBS_PACKAGE := scl-sourceguardian
include $(EATOOLS_BUILD_DIR)obs-scl.mk
