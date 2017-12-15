#!/bin/bash

# AUTHOR : MANIKYA SWATHI VALLABHAJOSYULA
# run the Tools to create the following:
# 1. Hearst IS-A pattern
# 2. Normalized Hearst Patterns
# 3. New Normalised Data
# 4. Creating Word Embeddings

CREATE_EMBED=true
EXTRACT_PAT=false

if $EXTRACT_PAT; then
    if [ -d "Data*" ]; then
	rm -R Data*
    fi
    # Python program to extract IS-A pattern
    # python toolname input_folder/ output_folder/
    mkdir DataHIsA
    chmod 777 DataHIsA
    python Hearst_Pattern_Stage2_IsA.py UMBC_webbase_sample/ DataHIsA/ &

    # Python program to normalise stage 1 Hearst Patterns
    # python toolname input_folder/ output_folder/
    mkdir DataNH
    chmod 777 DataNH
    python Hearst_Patterns_Stage2_Norm_6.py UMBC_webbase_sample/ DataNH/ &

    # Python program to create new normalization texts
    # python toolname input_folder/ output_folder/
    mkdir DataNN
    chmod 777 DataNN
    python Norlaization_Stage2.py UMBC_webbase_sample/ DataNN/ &
fi

wait

if $CREATE_EMBED; then
    mkdir DataNN_NH
    cp DataNN/* DataNN_NH/
    cp DataNH/* DataNN_NH/
    chmod -R 777 *
    # Python program to create word embeddings
    # python toolname input_folder output_filename
    python Create_word2vec_embedding.py DataNN_NH CBOW_w20_m10 &
fi

wait
