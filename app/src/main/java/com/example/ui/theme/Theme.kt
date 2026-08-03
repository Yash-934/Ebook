package com.example.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

@Composable
fun MyApplicationTheme(
  themeIndex: Int = 2,
  content: @Composable () -> Unit,
) {
  val colorScheme = when (themeIndex) {
      0 -> lightColorScheme(
          background = WhiteThemeBackground,
          surface = WhiteThemeBackground,
          onBackground = WhiteThemeText,
          onSurface = WhiteThemeText,
          primary = WhiteThemePrimary
      )
      1 -> darkColorScheme(
          background = DarkBlueThemeBackground,
          surface = DarkBlueThemeSurface,
          onBackground = DarkBlueThemeText,
          onSurface = DarkBlueThemeText,
          primary = DarkBlueThemePrimary
      )
      2 -> lightColorScheme(
          background = SepiaThemeBackground,
          surface = SepiaThemeSurface,
          onBackground = SepiaThemeText,
          onSurface = SepiaThemeText,
          primary = SepiaThemePrimary
      )
      3 -> darkColorScheme(
          background = BlackThemeBackground,
          surface = BlackThemeBackground,
          onBackground = BlackThemeText,
          onSurface = BlackThemeText,
          primary = BlackThemePrimary
      )
      else -> lightColorScheme()
  }

  MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
