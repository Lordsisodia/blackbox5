---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/colorfield",
    "fetched_at": "2026-02-10T13:29:40.592394",
    "status": 200,
    "size_bytes": 299538
  },
  "metadata": {
    "title": "ColorField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "colorfield"
  }
}
---

# ColorField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ColorFieldAsk assistantAllow users to select a color with a color picker or as a text input.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties)Properties[Anchor to alpha](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-alpha)alpha**alpha**boolean**boolean**Default: false**Default: false**Allow user to select an alpha value.

[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-autocomplete)autocomplete**autocomplete**"on" | "off"**"on" | "off"**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

The current value for the field. If omitted, the field will be empty.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91<s-color-field placeholder="Select a color" value="#FF0000" />## Preview### Examples- #### Codejsx```

<s-color-field placeholder="Select a color" value="#FF0000" />

```html```

<s-color-field placeholder="Select a color" value="#FF0000"></s-color-field>

```- #### Basic UsageDescriptionStandard color input field with hex value.jsx```

<s-stack gap="base">

<s-color-field label="Brand color" name="brandColor" value="#FF0000" />

</s-stack>

```html```

<s-stack gap="base">

<s-color-field label="Brand color" name="color" value="#FF0000"></s-color-field>

</s-stack>

```- #### RequiredDescriptionRequired color field ensuring essential color values are provided.jsx```

<s-stack gap="base">

<s-color-field label="Brand color" value="#FF0000" required />

</s-stack>

```html```

<s-stack gap="base">

<s-color-field label="Brand color" value="#FF0000" required></s-color-field>

</s-stack>

```- #### With Alpha TransparencyDescriptionColor field supporting alpha channel for transparency control.jsx```

<s-stack gap="base">

<s-color-field

label="Background color"

value="rgba(255, 0, 0, 0.5)"

alpha

/>

</s-stack>

```html```

<s-stack gap="base">

<s-color-field

label="Background color"

value="rgba(255, 0, 0, 0.5)"

alpha

></s-color-field>

</s-stack>

```- #### With Error StateDescriptionColor field with validation error for invalid color format inputs.jsx```

<s-stack gap="base">

<s-color-field

label="Brand color"

name="brandColor"

value="#invalid"

error="Please enter a valid color format (hex, rgb, or rgba)"

required

></s-color-field>

</s-stack>

```html```

<s-stack gap="base">

<s-color-field

label="Brand color"

name="brandColor"

value="#invalid"

error="Please enter a valid color format (hex, rgb, or rgba)"

required

></s-color-field>

</s-stack>

```- #### With Help TextDescriptionColor field with contextual details providing additional guidance.jsx```

<s-stack gap="base">

<s-color-field

label="Primary color"

value="#1a73e8"

details="Main brand color used for buttons and links"

/>

</s-stack>

```html```

<s-stack gap="base">

<s-color-field

label="Primary color"

value="#1a73e8"

details="Main brand color used for buttons and links"

></s-color-field>

</s-stack>

```- #### With PlaceholderDescriptionColor field demonstrating how to use a placeholder to guide user input for color selection.jsx```

<s-stack gap="base">

<s-color-field

label="Theme color"

placeholder="Enter a hex color (e.g., #FF0000)"

value="#000000"

/>

</s-stack>

```html```

<s-stack gap="base">

<s-color-field

label="Theme color"

placeholder="Enter a hex color (e.g., #FF0000)"

value="#000000"

></s-color-field>

</s-stack>

```- #### Read Only StateDescriptionColor field in a read-only mode, preventing user modifications to the color value.jsx```

<s-stack gap="base">

<s-color-field label="System color" name="color" value="#1a73e8" readOnly />

</s-stack>

```html```

<s-stack gap="base">

<s-color-field label="System color" name="color" value="#1a73e8" readOnly></s-color-field>

</s-stack>

```- #### Form IntegrationDescriptionA multi-color field form section demonstrating how ColorField can be used to capture different color settings in a single form.jsx```

<s-stack gap="base">

<s-section>

<s-heading>Theme settings</s-heading>

<s-stack gap="base">

<s-color-field

label="Primary brand color"

name="primaryColor"

value="#1a73e8"

defaultValue="#1a73e8"

details="This color will be used for buttons, links, and brand elements"

required

/>

<s-color-field

label="Secondary color"

name="secondaryColor"

value="#34a853"

details="Used for secondary actions and accents"

/>

<s-color-field

label="Background overlay"

name="overlayColor"

value="rgba(0, 0, 0, 0.5)"

alpha

details="Background color for modal overlays and dropdowns"

/>

</s-stack>

</s-section>

</s-stack>

```html```

<s-stack gap="base">

<s-section>

<s-heading>Theme settings</s-heading>

<s-stack gap="base">

<s-color-field

label="Primary brand color"

name="primaryColor"

value="#1a73e8"

defaultValue="#1a73e8"

details="This color will be used for buttons, links, and brand elements"

required

></s-color-field>

<s-color-field

label="Secondary color"

name="secondaryColor"

value="#34a853"

details="Used for secondary actions and accents"

></s-color-field>

<s-color-field

label="Background overlay"

name="overlayColor"

value="rgba(0, 0, 0, 0.5)"

alpha

details="Background color for modal overlays and dropdowns"

></s-color-field>

</s-stack>

</s-section>

</s-stack>

```- #### Color validationDescriptionInteractive example showing real-time hex color validation with error messages.jsx```

const [color, setColor] = useState('#invalid');

const [error, setError] = useState('Please enter a valid color format');

return (

<s-section>

<s-stack gap="base" justifyContent="start">

<s-text-field label="Theme name" />

<s-color-field

label="Brand color"

name="Color"

value={color}

error={error}

required

onInput={(e) => {

setColor(e.currentTarget.value);

setError(/^#([0-9A-F]{3}){1,2}$/i.test(e.currentTarget.value) ? '' : 'Please enter a valid color format');

}}

/>

</s-stack>

</s-section>

)

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/forms/colorfield#best-practices)Best practices

- Use the alpha property to allow merchants to select transparent colors

- Provide clear labels that indicate what the color will be used for

- Use details text to provide context about the color's purpose

- Validate color format inputs and provide clear error messages

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)