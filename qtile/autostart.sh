#!/bin/sh
nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = On }"
wal -r
picom & disown
nitrogen --restore 
