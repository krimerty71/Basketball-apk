[app]
title = Мячик Баскетбол
package.name = myachikbasket
package.domain = com.antoha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3,wav,ogg
version = 1.0
requirements = python3,kivy==2.1.0
orientation = portrait
fullscreen = 0

# Android settings
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.sdk = 23
android.ndk = 23b
android.accept_sdk_license = True

[buildozer]
log_level = 2
