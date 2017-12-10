#!/bin/bash

# AUTHOR : MANIKYA SWATHI VALLABHAJOSYULA

# COMMAND ARGUMNETS
# ARG 1 : WORD EMBEDIING MATRIX - UMBCNewNormNoStopHearst_CBOW_20_10 or UMBCNewNormNoStopHearst_SG_20_10
# ARG 2 : 1A.english.(training|trial).data.txt
# ARG 3 : PHI01 file name Phi01.txt
# ARG 4 : PHI02 file name Phi02.txt
python PhiModule.py UMBCNewNormNoStopHearst_CBOW_20_10 1A.english.trial.data.txt phi01.txt phi02.txt
