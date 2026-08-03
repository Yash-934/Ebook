package com.example.data

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore(name = "settings")

class SettingsManager(private val context: Context) {
    companion object {
        val DARK_MODE_ENABLED = booleanPreferencesKey("dark_mode_enabled")
        val CLOUD_SYNC_ENABLED = booleanPreferencesKey("cloud_sync_enabled")
        val FONT_SIZE = floatPreferencesKey("font_size")
    }

    val darkModeFlow: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[DARK_MODE_ENABLED] ?: false
    }

    val cloudSyncFlow: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[CLOUD_SYNC_ENABLED] ?: true
    }
    
    val fontSizeFlow: Flow<Float> = context.dataStore.data.map { preferences ->
        preferences[FONT_SIZE] ?: 16f
    }

    suspend fun setDarkMode(enabled: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[DARK_MODE_ENABLED] = enabled
        }
    }

    suspend fun setCloudSync(enabled: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[CLOUD_SYNC_ENABLED] = enabled
        }
    }

    suspend fun setFontSize(size: Float) {
        context.dataStore.edit { preferences ->
            preferences[FONT_SIZE] = size
        }
    }
}
