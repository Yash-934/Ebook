#!/bin/bash
sed -i 's/import androidx.compose.material.icons.filled.FormatUnderlinedBorder//' app/src/main/java/com/example/ui/screens/ReadScreen.kt
sed -i 's/Icons.Default.Highlight/Icons.Default.BorderColor/' app/src/main/java/com/example/ui/screens/ReadScreen.kt
sed -i 's/containerColor = bgColor/containerColor = backgroundColor/' app/src/main/java/com/example/ui/screens/ReadScreen.kt
