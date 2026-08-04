#!/bin/bash
cat << 'INNER_EOF' > replacement.txt
                                        currentLineColor = when (activeEditTool) {
                                            "highlight" -> highlightColor
                                            "underline" -> underlineColor
                                            else -> doodleColor
                                        }
INNER_EOF

# Replace the currentLineColor logic
sed -i '/currentLineColor = when (activeEditTool) {/,/}/c\'"$(cat replacement.txt)"'' app/src/main/java/com/example/ui/screens/ReadScreen.kt
