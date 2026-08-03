package com.example.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.SettingsManager
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class SettingsViewModel(private val settingsManager: SettingsManager) : ViewModel() {
    val darkModeEnabled: StateFlow<Boolean> = settingsManager.darkModeFlow.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = false
    )

    val cloudSyncEnabled: StateFlow<Boolean> = settingsManager.cloudSyncFlow.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = true
    )

    val fontSize: StateFlow<Float> = settingsManager.fontSizeFlow.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = 16f
    )

    fun toggleDarkMode(enabled: Boolean) {
        viewModelScope.launch { settingsManager.setDarkMode(enabled) }
    }

    fun toggleCloudSync(enabled: Boolean) {
        viewModelScope.launch { settingsManager.setCloudSync(enabled) }
    }

    fun setFontSize(size: Float) {
        viewModelScope.launch { settingsManager.setFontSize(size) }
    }
}

class SettingsViewModelFactory(private val settingsManager: SettingsManager) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(SettingsViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return SettingsViewModel(settingsManager) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
