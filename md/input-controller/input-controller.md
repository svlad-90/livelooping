[Go to the previous page](../../README.md#sub-articles)

----

# Table of contents

- ["Input controller" logical device](#input-controller-logical-device)
  * [Selecting the preset page](#selecting-the-preset-page)
  * [Selecting the preset](#selecting-the-preset)
  * [Changing the volume level](#changing-the-volume-level)
  * [Changing the FX level](#changing-the-fx-level)
  * [Saving the preset](#saving-the-preset)
  * [Deleting the preset](#deleting-the-preset)
  * [Creating and editing the preset](#creating-and-editing-the-preset)
    * [VST parameters](#vst-parameters)
	* [VST activation statuses](#vst-activation-statuses)
	* [Active FX unit](#active-fx-unit)
	* [MIDI mapping](#midi-mapping)
  * [What is used as a persistency for the presets?](#what-is-used-as-a-persistency-for-the-presets)
  * [Applying Turnado effect to the input controller](#applying-turnado-effect-to-the-input-controller)
	* [Changing the Turnado dictator value](#changing-the-turnado-dictator-value)
	* [Changing the Turnado Dry/Wet value](#changing-the-turnado-dry-wet-value)
	* [Randomizing Turnado](#randomizing-turnado)
	* [Switching between the Turnado VST presets](#switching-between-the-turnado-vst-presets)
  * [FX parameters](#fx-parameters)
    * [Changing FX parameter values](#changing-fx-parameter-values)
    * [FX units](#fx-units)
	* [Changing the active FX unit](#changing-the-active-fx-unit)
	* [Switching the FX unit presets](#switching-the-fx-unit-presets)
	* [Assigning MIDI mapping](#assigning-midi-mapping)
	* [Deleting MIDI mapping](#deleting-midi-mapping)
----

# "Input controller" logical device

![Looper mux view](../screenshots/input-controller.jpg)

The "input controller" logical device is something, that works with your input audio signal before it reaches the [looper mux](../looper-mux/looper-mux.md). It's purpose is to replace your "second device", e.g. Helix Line 6, Boss GT10b, etc.

The **LIVELOOPING** project supports 2 instances of the "input controller" logical device. Meaning that you can independently operate on 2 instruments:

![Logical devices schema](./resources/logical-devices-schema.jpg)

For sure, it is not mandatory to use the second instance of the "input controller" device.

E.g. if you perform purely as "beatbox-only" and "everything from the mouth" artist, it will be sufficient for you to use only one instance.

----

## Selecting the preset page

"Input controller" logical device consists of the **4 preset pages**. Each preset page can store **8 presets**. In sum, the user can store **32 different presets** .

Which information is part of the preset will be described in a dedicated section.

In order to select the preset page, use the **"Hold + X"** short-cut on the corresponding KP3+ device, where X represents the number of the page:

![Selecting the preset page](./resources/selecting-the-preset-page.jpg)

The view will reflect the selection within the DAW in the following way:

![Preset page selected](./resources/preset-page-selected.jpg)

----

## Selecting the preset

In order to select the preset use the **1-8** digits:

![Selecting the preset](./resources/selecting-the-preset.jpg)

The view will reflect the selection within the DAW in the following way:

![The preset selected](./resources/preset-selected.jpg)

Selecting the preset applies the stored preset's parameters. As some of them are visible in the view, their values will be also updated:

![Updated parameter values](./resources/updated-parameter-values.jpg)

----

## Changing the volume level

You can change the volume level of the instrument, using the **Level** fader of the KP3+:

![Changing the instrument volume](./resources/changing-instrument-volume.jpg)

The view will reflect the input within the DAW in the following way:

![Instrument volume changed](./resources/instrument-volume-changed.jpg)

----

## Changing the FX level

You can change the FX level, which is applied to the instrument, using the **"Hold + Level"** short-cut on the KP3+ side:

![Changing the FX level](./resources/changing-fx-level.jpg)

The view will reflect the input within the DAW in the following way:

![FX level changed](./resources/fx-level-changed.jpg)

**Note!** FX level excludes Dry/Wet level of the Turnado VST. That one is handled by a separate knob.

----

## Saving the preset

The user has possibility to adjust the preset settings in order to achieve the desired sound.

Once all settings are specified, you can save the preset in the following way:

- Press **"Hold + 5"** short-cut on the KP3+ to activate the **"Save mode"**:

  ![Activating save mode](./resources/activating-save-mode.jpg)

  The view will reflect entrance to the **"Save mode"**:

  ![Entered the save mode](./resources/entered-save-mode.jpg)

- If needed, [select the target preset page](#selecting-the-preset-page) as usual.

- [Select the target preset](#selecting-the-preset). 

  **Selecting the preset in the "Save mode" will cause the data to be saved into the selected slot.**

  After the preset is saved, the view will represet, that there is some data available in the slot, meaning that it is not empty anymore:
  
  ![Not empty preset slot](./resources/not-empty-preset-slot.jpg)

----

## Deleting the preset

User can not only save new preset, but also delete the existing one.

You can delete the preset in the following way:

- Press **"Hold + 6"** short-cut on the KP3+ to activate the **"Delete mode"**:

  ![Activating delete mode](./resources/activating-delete-mode.jpg)

  The view will reflect entrance to the **"Save mode"**:

  ![Entered the delete mode](./resources/entered-delete-mode.jpg)

- If needed, [select the target preset page](#selecting-the-preset-page) as usual.

- [Select the target preset](#selecting-the-preset). 

  **Selecting the preset in the "Delete mode" will cause the data to be deleted from the selected slot.**

  After the preset is deleted, the view will represet, that there is no more data available in the slot, meaning that it is empty:
  
  ![Empty preset slot](./resources/empty-preset-slot.jpg)

----

## Creating and editing the preset

This section will describe what the **LIVELOOPING** project's preset is and how to create and edit it.

The preset consists of the following types of data:

- **All parameters of all the VST plugins, which are located in the FX_CHANNEL mixer channel of the "input controller"**
- **The selected active FX unit**
- **The MIDI mapping of the custom FX unit**

More details regarding each stored data type are shown below.

----

### VST parameters

The list of the VST plugins includes the following one:

![Preset VST plugins](./resources/preset-plugins.jpg)

|Used VST plugin|Purpose|
|---|---|
|FabFilter Pro-Q 3|Advanced EQ|
|FIN-VOOD|Quite powerful and easy to use effects processor|
|Manipulator|Ultimate voice transformer|
|Fruity Fast Dist|Low latency distortion|
|Stereo enhancer|Basic stereo effect|
|Fruity reverb 2|Reverb effect|
|Fruity delay 2|Delay effect|
|Fruity filter|Filter effect|
|Fruity compressor|Compressor|
|Fuity Limiter|Limiter|

From my experience, the above list is enough to create a wide range of different sounds. The live_looping.flp project already comes with several dozens of saved presets. Try it out!

**Still, if there would be a need from the audience to extend the number of the supported plugins - I can add one more fx channel with another 10 effects. Also we can think of more  generic mechanism to replace the used VST plugins.**

**Note!** As of now you can't change the order or exchange the elements of the list without touching the source code. And without loosing already saved presets.

Currently, first instance of the input controller is using mixer channel **#5** as the  **FX_CHANNEL**. The second instance is using the mixer channel **#9** as the **FX_CHANNEL**:

![FX channels](./resources/fx_channels.jpg)

**Q: So, tell me at last, what should I do to change the parameters? Anything complex?**

**A: NO! Simply open the plugins within the above-mentioned mixer channels in the DAW, and play around with the parameters. As soon as sound fits to your needs - [save the preset](#saving-the-preset) as usual.**

The implementation of the project will traverse all values of all the parameters, and will store them to persistency.

----

### VST activation statuses

**TODO**: Revisit this flow to simplify it.

Each VST from the [above section](#vst-parameters) can be enabled or disabled.

Unfortunately, the way to change the activation status of the VST effects is not the most comfortable one. 

In order to change it, do the following:

- Open the mixer

  ![Opening the mixer](./resources/opening-the-mixer.jpg)

- Open the input controller's instance main mixer channel:

  |Instance id|Main mixer channel number|
  |---|---|
  |#1|6|
  |#2|10|

  ![Input controller main mixer channels](./resources/input-controller-main-mixer-channels.jpg)

- Open the MIDI routing view:

  ![Opening MIDI routing view](./resources/opening-midi-routing-view.jpg)

- Change the VST activation status clicking on one of the **E1_TO - E10_TO** buttons:

  ![Changing VST activation status](./resources/changing-vst-activation-status.jpg)

- [Change the FX level](#changing-the-fx-level) on KP3+ to apply the change

Once again, we will revisit this section soon.

----

### Active FX unit

  ![Active FX unit](./resources/active-fx-unit.jpg)

  You can check what is the FX unit [here](#fx-units). For this section it's only important to know that active fx unit type is also the part of the stored pattern.

----

### MIDI mapping

  MIDI mapping data is also saved as part of the dedicated preset.
  
  You can read more on what is the MIDI mapping [here](#assigning-midi-mapping). For this section it's only important to know that midi mapping is also the part of the stored pattern.

----

## What is used as a persistency for the presets?

**Note!** This section describes an implementation detail. It provides no useful information for the average user. Still, it allows to avoid confusion for the users, which would like to deeply investigate the **LIVELOOPING's** flp project.

This is an interesting question. Actually, FL Studio does not ship the io python module inside its python interpreter. So there is no way to store any data to the file-system.

But we've found the way out. 

The name of the tracks in the playlist of the DAW is used to save all the data. You can see it yourself. Just:

- Open the playlist:

  ![Opening the playlist](./resources/opening-playlist.jpg)

- Scroll to the track 100 or 200. See the track names:

  ![The stored data](./resources/stored-data.jpg)

  Range 100-200 is reserved for the needs of the first "input controller' logical device. Range 200-300 is reserved for the needs of the second "input controller' logical device.

Actually, there is a lot of data inside each track name:

```
{'PLUGIN_PARAMS': {10: ['1.0', '1.0', '0.0', '0.0', '0.0', '1.0', '1.0', '0.0', '1.0', '1.0'], 0: ['1.0', '1.0', '0.31585195660591125', '0.6239166855812073', '0.20491667091846466', '1.0', '1.0', '0.5272108316421509', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '1.0', '1.0', '0.8641238808631897', '0.6380952000617981', '0.3851388692855835', '1.0', '1.0', '0.6069444417953491', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '1.0', '1.0', '0.5554232001304626', '0.6632652878761292', '0.355611115694046', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '1.0', '1.0', '0.22962868213653564', '0.0', '0.5', '1.0', '1.0', '0.5317777991294861', '0.25', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '1.0', '0.5751884579658508', '0.5', '0.5', '1.0', '1.0', '0.5', '0.0', '0.1111111119389534', '0.5', '0.10000000149011612', '0.0', '0.0', '0.25', '0.5', '0.5', '0.5', '0.0', '0.0', '0.0', '0.0', '1.0', '1.0', '1.52587890625e-05', '0.5', '0.6666666865348816', '0.5', '0.75', '0.0', '1.0', '1.0', '1.0', '0.0', '0.5', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0'], 1: ['0.6309999823570251', '0.6309999823570251', '0.5510203838348389', '0.0', '0.4881889820098877', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0'], 2: ['0.0', '0.25', '0.5', '0.8732812404632568', '0.11339999735355377', '0.2445833384990692', '1.0', '1.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.0', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5121874809265137', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.5', '0.0', '0.0', '0.0', '0.0', '1.0', '1.0', '1.0', '1.0', '0.2666666805744171', '0.5', '0.2666666805744171', '0.5', '0.2666666805744171', '0.5', '0.2666666805744171', '0.5', '0.0', '0.2666666805744171', '0.5', '0.2666666805744171', '0.0', '0.2666666805744171', '0.5', '0.2666666805744171', '0.0', '0.2666666805744171', '0.5', '0.2666666805744171', '0.0', '0.2666666805744171', '0.5', '0.2666666805744171', '0.0', '0.0', '0.0', '0.0', '0.33799999952316284', '0.0', '0.30094006657600403', '0.6247779130935669', '0.33799999952316284', '0.0', '0.33799999952316284', '0.0', '1.0', '0.0', '1.0', '0.0', '1.0', '0.0', '1.0', '0.0', '0.5', '0.6913415193557739', '0.8535534739494324', '0.9619399905204773', '1.0', '0.9619399905204773', '0.8535534739494324', '0.6913415193557739', '0.5', '0.30865851044654846', '0.2603493332862854', '0.32477864623069763', '0.0', '0.32478293776512146', '0.2603493332862854', '0.30865851044654846', '1.0', '0.0', '0.8535534739494324', '0.0', '1.0', '0.0', '0.9807692170143127', '0.0', '0.7884615659713745', '0.0', '0.8461538553237915', '0.0', '1.0', '0.0', '1.0', '0.30865851044654846', '0.5', '0.6913415193557739', '0.8535534739494324', '0.9619399905204773', '1.0', '0.9619399905204773', '0.8535534739494324', '0.6913415193557739', '0.5', '0.30865851044654846', '0.2603493332862854', '0.32477864623069763', '0.0', '0.32478293776512146', '0.2603493332862854', '0.30865851044654846', '0.5', '0.6913415193557739', '0.8535534739494324', '0.9619399905204773', '1.0', '0.9619399905204773', '0.8535534739494324', '0.6913415193557739', '0.5', '0.30865851044654846', '0.2603493332862854', '0.32477864623069763', '0.0', '0.32478293776512146', '0.2603493332862854', '0.30865851044654846', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '1.0', '1.0', '0.75', '1.0', '1.0', '0.0', '0.0', '0.5', '0.5', '0.0', '0.0', '1.0', '0.0', '0.0', '0.0', '0.0', '0.0'], 3: ['0.5', '0.4444444444444444', '0.0', '0.8359375', '0.8671875'], 4: ['0.5', '0.8', '0.5', '0.3466796875', '1.0', '0.0'], 5: ['0.018785642401878563', '0.16203703703703703', '0.0', '0.494949494949495', '1.0', '0.06030150753768844', '0.16203703703703703', '0.2857142857142857', '0.24050632911392406', '0.5', '0.8', '0.4', '0.2125', '0.333984375', '0.0'], 6: ['0.015625', '0.475', '0.8', '0.14960629921259844', '0.12385919165580182', '0.5', '1.0', '1.0'], 7: ['0.982421875', '0.0', '1.0', '1.0', '1.0', '0.0'], 8: ['0.47333333333333333', '0.25675675675675674', '0.7283333333333334', '0.0375', '0.04976244061015254', '0.0'], 9: ['0.589', '1.0', '0.5', '0.1115', '0.2857142857142857', '0.5', '0.2857142857142857', '0.2882', '1.0', '0.5', '0.5', '0.0', '0.6666', '0.0', '0.065', '1.0', '0.0', '0.4187']}, 'MIDI_MAPPING': {0: [1, 4], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1], 4: [-1, -1], 5: [-1, -1], 6: [-1, -1], 7: [-1, -1]}, 'ACTIVE_FX_UNIT': 0, 'VERSION': 1.0}
```

Actually, we are lucky that FL studio team made this field unlimited in size. Otherwise, it would not be possible to store any data as aprt of the project.

I hope thay'll never change it :)

----

## Applying Turnado effect to the input controller

The idea behind the Turnado VST is the following one:
- Turnado provides 24 different effects.
- Out of those 24 effects you can select 8 active effects and fine-tune them.
- Turnado has a "dictator" killing feature, which allows you to manipulate 8 active effects with one single fader.
- This VST has a "randomize" option, which can randomly change everything - active effects, their setting, settings of the dictator fader.

Each input controller instance has an instance of Turnado VST being built in.

----

### Changing the Turnado dictator value

In order to change the turnado dictator value, use the **"FX DEPTH"** knob on the KP3+:

![Changing turnado dictator level](./resources/changing-turnado-dictator-level.jpg)

Changing that parameter will do the following thing on Turnado's side:

![Turnado dictator usage](./resources/turnado-dictator.gif)

The view will reflect this in the following way within the DAW:

![Turnado dictator level changed](./resources/turnado-dictator-level-changed.jpg)

----

### Changing the Turnado Dry-Wet value

In order to change the turnado dictator value, use the **"Hold + FX DEPTH"** shortcut on the KP3+:

![Changing turnado Dry/Wet value](./resources/changing-turnado-dry-wet-value.jpg)

Alternatively you can use the **"C"** button to instantly switch the Dry/Wet value between 0 and 100:

![Instant turnado Dry/Wet on off](./resources/instant-turnado-on-off.jpg)

In both cases the view will reflect this in the following way within the DAW:

![Turnado dictator level changed](./resources/turnado-dictator-dry-wet-changed.jpg)

Also, 0 Dry/Wet level is considered as "Off mode" by the view:

![Turnado off mode](./resources/turnado-off-mode.jpg)

----

### Randomizing Turnado

In order to randomize the Turnado use the **"double-click on the Hold button"** short-cut:

![Randomizing turnado](./resources/randomizing-turnado.jpg)

The short-cut will change the selected effects, their settings, and split between effects within the dictator section.

The view does not reflect that. There seems to be no real reason to visualize that.

**Note!** in order to Randmize function to work, you need to have Turnado instance be **IN FOREGROUND** within the DAW. That's why you'll find all Turnado instances being hidden somewhere in the right bottom corner of the screen, while still being in foreground. It is by intention. Do not close them.

----

### Switching between the Turnado VST presets

"Randomize" option is quite handy, but sometimes it gives unpredictable results.

Thus, it is more common to switch between the fine-tuned pre-saved presets. In order to do that, one could use **"A"** and **"B"** buttons:

![Switching turnado between presets](./resources/turnado-switch-between-presets.jpg)

In the view, the corresponding buttons will blink in case of usage:

![Turnado switched to the previous pattern](./resources/turnado-previous-pattern-selected.jpg)

![Turnado switched to the next pattern](./resources/turnado-next-pattern-selected.jpg)

**Note!** The presets mentioned here are simple VST presets. They are not the composite presets implemented by the **LIVELOOPING** project.

----

## FX parameters

The possibility to save complex patterns and instantly switch between them is awesome. But it is not eanough. You should be able to manipulate with the selected sound at realtime, in order to add additional diversity.

In order to do this you can use 8 FX parameters:

![FX parameters](./resources/fx-parameters.jpg)

Depending on the confitions, which are described [here](#fx-units), those parameters can be assigned to different control elements of the VST plugins.

----

### Changing FX parameter values

In order to change the FX parameter values, use 8 virtual faders on the touch-screen:

![Changing FX parameters](./resources/changing_fx_parameters.jpg)

The view will reflect the changes accordingly.

----

### FX units

Active FX unit represents, which set of VST parameters are assigned to the FX parameters of the logical device at current moment.

Currently there are 3 supported FX unit types available:

![Active FX unit](./resources/active-fx-unit.jpg)

Here is a brief description of each FX unit type:

|FX unit type|Comment|
|---|---|
|Manipulator|FX parameters are associated with the Manipulator VST instance|
|Voodoo Finisher|FX parameters are associated with the Voodoo Finisher VST instance|
|Custom|FX parameters are assigned manually by the user. The mapping is persisted as part of the preset.|

Here is description of the mapping between the VST parameters and FX parameters used in each FX unit:

#### Manipulator FX unit

|Parameter id|Parameter name|
|---|---|
|1|Formant|
|2|Pitch|
|3|Ratio|
|4|Harmonics|
|5|FM|
|6|Alternator|
|7|Octave|
|8|Wet/Dry|

#### Voodoo Finisher FX unit

|Parameter id|Parameter name|
|---|---|
|1|Variation 1|
|2|Variation 2|
|3|Variation 3|
|4|Variation 4|
|5|Not used|
|6|Not used|
|7|Not used|
|8|Wet/Dry|

#### Custom FX unit

The idea of the custom FX unit type is that user has a possibility to assign MIDI mapping to any of the parameters within the [list of the device's VST-s](#vst-parameters). So table here would look like this:

|Parameter id|Parameter name|
|---|---|
|1|Assigned by the user|
|2|Assigned by the user|
|3|Assigned by the user|
|4|Assigned by the user|
|5|Assigned by the user|
|6|Assigned by the user|
|7|Assigned by the user|
|8|Assigned by the user|

----

### Changing the active FX unit

The selected mapping is persisted as part of the preset. So you can select different parameters for each created preset.

To change the active FX unit use the **"D"** button on the KP3+:

![Changing the active FX unit](./resources/changing-active-f-unit.jpg)

The view will reflect the change in the DAW. An active FX unit will be highlighted:

![Active FX unit changed](./resources/active-fx-unit-changed.jpg)

----

### Switching the FX unit presets

The described above **"Manipulator"** and **"Voodoo Finisher"** fx unit types have one to one relation to VST plugins with the same names.

That means, that when working in those modes, it would be useful for the user to be able to change the presets of those VST-s without touching the DAW.

**LIVELOOPING** project implements such possibility. User can jump between the presets of the 2 above-mentioned VST plugins, using:
  - **"Hold + 8"** short-cut on KP3+ to select the next VST preset
  - **"Hold + 7"** short-cut on KP3+ to select the previous VST preset

![Switching the FX unit type presets](./resources/switching-fx-unit-type-presets.jpg)

Such feature allows the following workflow:

- [Select the active fx unit type](#changing-the-active-fx-unit), Choose **"Manipulator"** or **"Voodoo Finisher"**. For **"Custom"** this feature has no effect.
- Jump between the presets and select one as a base-line for your sound idea
- [Play around with the FX parameter values](#changing-fx-parameter-values) to fine tune the sound
- [Save the preset](#saving-the-preset)

----

### Assigning MIDI mapping

As mentioned [here](#custom-fx-unit), when user selects the "custom" fx unit type, he is capable of assigning individual MIDI mappings to the VST parameters. This section describes such a procedure.

**Note!** FYI. This paragraph is the advanced one. You will not need to modify any source code to proceed. But, as the possibilities of the DAW's view are limited, the part of the interaction within this scenario would be done in the "script output" console.

Let's imagine, that I want to assign the Reverb's VST Wet level to the FX parameter **#2**. 

In order to achieve that, let's follow such a steps:

- Open the "script output" console:

  ![Opening the script output console](./resources/opening-script-output-console.jpg)

  Place it in a way that you see both the console and the target logical device on the screen.

- Select the tab with the target device. It would be either the one with the output from "device_KorgKaossPad3Plus_MicController" class or from "device_KorgKaossPad3Plus_SynthController" class. Specific tab depends on the instance of the "input controller" logical device, which you are using:

  ![Script output console](./resources/script-output-console.jpg)

- Enter the "Midi mapping save mode" using the **"Hold + double click on digit 5"** short-cut on the KP3+:

  ![Activating MIDI mapping save mode](./resources/activating-midi-mapping-save-mode.jpg)

  The view will reflect this in the DAW in the following way:

  ![MIDI mapping save mode activated](./resources/midi-mapping-save-mode-activated.jpg)

  On top of that you'll see the following message in the console:
  
  ```
  MIDI mapping input dialog >>> Please, enter fx parameter number.
  ```

- Select the target fx parameter, using the **1-8** digits on the KP3+:

  ![Selecting the target preset slot](./resources/selecting-the-target-preset-slot.jpg)

  I've selected the slot **#2**.
  
  After the slot is selected, you'll see the following messages in the console:
  
  ```
  MIDI mapping input dialog >>> Fx parameter number '1' was selected
  MIDI mapping input dialog >>> Please, select the target plugin
  MIDI mapping input dialog >>> Current cursor position is - #0 'FabFilter Pro-Q 3'
  ```

- Select the target VST plugin. Use the following controls on the KP3+ to navigate: 
  
  |Control|Meaning|
  |---|---|
  |**"A"**|Previous item|
  |**"B"**|Next item|
  |**"C"**|Select item and proceed to the next step|
  |**"D"**|Cancel the operation| 

  ![Navigation within the items list](./resources/navigating-within-the-items-list.jpg)

  In my case, I've pressed **"B + B + B + B + B + C"** to select the "Fruity Reverb 2" VST. I've seen the following output in the console:
  
  ```
  MIDI mapping input dialog >>> Current cursor position is - #1 'FIN-VOOD'
  MIDI mapping input dialog >>> Current cursor position is - #2 'Manipulator'
  MIDI mapping input dialog >>> Current cursor position is - #3 'Fruity Fast Dist'
  MIDI mapping input dialog >>> Current cursor position is - #4 'Fruity Stereo Enhancer'
  MIDI mapping input dialog >>> Current cursor position is - #5 'Fruity Reeverb 2'
  MIDI mapping input dialog >>> Plugin #5 'Fruity Reeverb 2' was selected
  MIDI mapping input dialog >>> Please, select the target parameter
  MIDI mapping input dialog >>> Current cursor position is - #0 'Low cut'
  ```

- Select the target VST parameter. The navigation is totally the same as in the previous point.

  I've pressed **"B"** until I've scrolled to the parameter #12 'Wet level'. Then I've pressed **"C"**. I've seen the following output in the console:
  
  ```
  MIDI mapping input dialog >>> Current cursor position is - #1 'High cut'
  MIDI mapping input dialog >>> Current cursor position is - #2 'Predelay'
  MIDI mapping input dialog >>> Current cursor position is - #3 'Room size'
  MIDI mapping input dialog >>> Current cursor position is - #4 'Diffusion'
  MIDI mapping input dialog >>> Current cursor position is - #5 'Decay time'
  MIDI mapping input dialog >>> Current cursor position is - #6 'High damping'
  MIDI mapping input dialog >>> Current cursor position is - #7 'Bass multiplier'
  MIDI mapping input dialog >>> Current cursor position is - #8 'Crossover'
  MIDI mapping input dialog >>> Current cursor position is - #9 'Stereo separation'
  MIDI mapping input dialog >>> Current cursor position is - #10 'Dry level'
  MIDI mapping input dialog >>> Current cursor position is - #11 'Early reflection level'
  MIDI mapping input dialog >>> Current cursor position is - #12 'Wet level'
  MIDI mapping input dialog >>> Parameter #12 'Wet level' was selected
  device_KorgKaossPad3Plus_MicController: setMidiMappingSaveMode: midi mapping save mode - False
  ```

- The MIDI mapping was already assigned at this stage. The FX parameter slot will become "non-empty". The level of the parameter would be fetched from the VST plugin:

  ![MIDI mapping assigned](./resources/midi-mapping-assigned.jpg)

  You can open the Reverb VST and check out, that changing the FX parameter 2 has effect on the Reverb level:

  ![MIDI mapping check](./resources/midi-mapping-check.gif)

- If you like the created MIDI mapping - **DO NOT FORGET TO [SAVE THE PRESET](#saving-the-preset)**. Only after that the MIDI mapping data will be persistently stored.

----

### Deleting MIDI mapping

**Note!** Read [this previous paragraph](#assigning-midi-mapping) to understand what we are talking about.

Let's imagine, that I want to delete MIDI mapping, which I've created [at the previous step](#assigning-midi-mapping).

In order to achieve that:

- Do all the steps from the [the previous paragraph](#assigning-midi-mapping) up to **SELECTING THE TARGET FX PARAMETER**.

- press the **"Hold + 6"** short-cut on the KP3+:

  ![MIDI mapping check](./resources/deleting-midi-mapping.jpg)

  That will delete the MIDI mapping. You'll see the following message in the console:
  
  ```
  MIDI mapping input dialog >>> Mapping was deleted.
  ```

  The FX parameter slot will become empty in the view:
  
  ![MIDI mapping empty slot](./resources/midi-mapping-empty-slot.jpg)

----

[Go to the previous page](../../README.md#sub-articles)