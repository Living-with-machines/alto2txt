#!/bin/bash
# warning: is destructive
# run from root data directory

for Publication in *; do
    if [[ -d $Publication ]]; then
        cd $Publication

        for Year in *; do
            if [[ -d $Year ]]; then
                cd $Year

                for Issue in *; do
                    if [[ -d $Issue ]]; then
                        cd $Issue
                        zip -9 $Issue.zip *.xml
                        rm *.xml
                        cd ..
                    fi
                done

                cd ..
           fi
        done

        cd ..
    fi
done
