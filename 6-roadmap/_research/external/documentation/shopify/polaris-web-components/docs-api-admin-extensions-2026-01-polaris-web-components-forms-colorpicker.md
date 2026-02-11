---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/colorpicker",
    "fetched_at": "2026-02-10T13:29:43.300278",
    "status": 200,
    "size_bytes": 252439
  },
  "metadata": {
    "title": "ColorPicker",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "colorpicker"
  }
}
---

# ColorPicker

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ColorPickerAsk assistantAllow users to select a color from a color palette.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#properties)Properties[Anchor to alpha](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#properties-propertydetail-alpha)alpha**alpha**boolean**boolean**Default: false**Default: false**Allow user to select an alpha value.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to formResetCallback](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#properties-propertydetail-formresetcallback)formResetCallback**formResetCallback**() => void**() => void**[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#properties-propertydetail-value)value**value**string**string**The currently selected color.

Supported formats include:

- HSL

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91<s-color-picker value="#FF0000" alpha />## Preview### Examples- #### Codejsx```

<s-color-picker value="#FF0000" alpha />

```html```

<s-color-picker value="#FF0000" alpha></s-color-picker>

```- #### Basic usageDescriptionDemonstrates a simple color picker with a pre-selected red color, showing the basic implementation without alpha transparency.jsx```

<s-box padding="large" border="base" borderRadius="base">

<s-color-picker value="#FF0000" name="primary-color" />

</s-box>

```html```

<s-box padding="large" border="base" borderRadius="base">

<s-color-picker value="#FF0000" name="primary-color"></s-color-picker>

</s-box>

```- #### With alpha transparencyDescriptionIllustrates a color picker with alpha transparency enabled, allowing selection of colors with varying opacity levels.jsx```

<s-box padding="large" border="base" borderRadius="base">

<s-color-picker

value="#FF0000FF"

alpha

name="color-with-alpha"

/>

</s-box>

```html```

<s-box padding="large" border="base" borderRadius="base">

<s-color-picker

value="#FF0000FF"

alpha

name="color-with-alpha"

></s-color-picker>

</s-box>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorpicker#best-practices)Best practices

- Use the alpha slider if you want to allow merchants to select a transparent color

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)