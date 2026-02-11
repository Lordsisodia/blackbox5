---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/numberfield",
    "fetched_at": "2026-02-10T13:30:00.049016",
    "status": 200,
    "size_bytes": 293882
  },
  "metadata": {
    "title": "NumberField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "numberfield"
  }
}
---

# NumberField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# NumberFieldAsk assistantCollect numerical values from users with optimized keyboard settings and built-in validation.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties)Properties[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-autocomplete)autocomplete**autocomplete**"on" | "off" | NumberAutocompleteFieldNumberAutocompleteField | `section-${string} one-time-code` | `section-${string} cc-number` | `section-${string} cc-csc` | "shipping one-time-code" | "shipping cc-number" | "shipping cc-csc" | "billing one-time-code" | "billing cc-number" | "billing cc-csc" | `section-${string} shipping one-time-code` | `section-${string} shipping cc-number` | `section-${string} shipping cc-csc` | `section-${string} billing one-time-code` | `section-${string} billing cc-number` | `section-${string} billing cc-csc`**"on" | "off" | NumberAutocompleteFieldNumberAutocompleteField | `section-${string} one-time-code` | `section-${string} cc-number` | `section-${string} cc-csc` | "shipping one-time-code" | "shipping cc-number" | "shipping cc-csc" | "billing one-time-code" | "billing cc-number" | "billing cc-csc" | `section-${string} shipping one-time-code` | `section-${string} shipping cc-number` | `section-${string} shipping cc-csc` | `section-${string} billing one-time-code` | `section-${string} billing cc-number` | `section-${string} billing cc-csc`**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to inputMode](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-inputmode)inputMode**inputMode**"decimal" | "numeric"**"decimal" | "numeric"**Default: 'decimal'**Default: 'decimal'**Sets the virtual keyboard.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to max](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-max)max**max**number**number**Default: Infinity**Default: Infinity**The highest decimal or integer to be accepted for the field. When used with `step` the value will round down to the max number.

Note: a user will still be able to use the keyboard to input a number higher than the max. It is up to the developer to add appropriate validation.

[Anchor to min](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-min)min**min**number**number**Default: -Infinity**Default: -Infinity**The lowest decimal or integer to be accepted for the field. When used with `step` the value will round up to the min number.

Note: a user will still be able to use the keyboard to input a number lower than the min. It is up to the developer to add appropriate validation.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to prefix](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-prefix)prefix**prefix**string**string**Default: ''**Default: ''**A value to be displayed immediately before the editable portion of the field.

This is useful for displaying an implied part of the value, such as "https://" or "+353".

This cannot be edited by the user, and it isn't included in the value of the field.

It may not be displayed until the user has interacted with the input. For example, an inline label may take the place of the prefix until the user focuses the input.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to step](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-step)step**step**number**number**Default: 1**Default: 1**The amount the value can increase or decrease by. This can be an integer or decimal. If a `max` or `min` is specified with `step` when increasing/decreasing the value via the buttons, the final value will always round to the `max` or `min` rather than the closest valid amount.

[Anchor to suffix](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-suffix)suffix**suffix**string**string**Default: ''**Default: ''**A value to be displayed immediately after the editable portion of the field.

This is useful for displaying an implied part of the value, such as "@shopify.com", or "%".

This cannot be edited by the user, and it isn't included in the value of the field.

It may not be displayed until the user has interacted with the input. For example, an inline label may take the place of the suffix until the user focuses the input.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

### NumberAutocompleteField```

'one-time-code' | 'cc-number' | 'cc-csc'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/numberfield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy912345678<s-number-field  label="Quantity"  details="Number of items in stock"  placeholder="0"  step={5}  min={0}  max={100}/>## Preview### Examples- #### Codejsx```

<s-number-field

label="Quantity"

details="Number of items in stock"

placeholder="0"

step={5}

min={0}

max={100}

/>

```html```

<s-number-field

label="Quantity"

details="Number of items in stock"

placeholder="0"

step="5"

min="0"

max="100"

></s-number-field>

```- #### Basic usageDescriptionDemonstrates a simple number field for entering order quantity with a predefined range and step value.jsx```

<s-number-field

label="Order quantity"

value="5"

min={1}

max={999}

step={1}

/>

```html```

<s-number-field

label="Order quantity"

value="5"

min="1"

max="999"

step="1"

></s-number-field>

```- #### With prefix and suffixDescriptionIllustrates a number field for entering product prices with currency prefix and suffix, using decimal input mode.jsx```

<s-number-field

label="Product price"

value="29.99"

prefix="$"

suffix="CAD"

inputMode="decimal"

step={0.01}

min={0}

/>

```html```

<s-number-field

label="Product price"

value="29.99"

prefix="$"

suffix="CAD"

inputMode="decimal"

step="0.01"

min="0"

></s-number-field>

```- #### Multiple examplesDescriptionShowcases multiple number fields for different use cases: inventory tracking, percentage discount, and shipping weight, demonstrating various input modes and configurations.jsx```

<s-stack gap="base">

<s-number-field

label="Inventory count"

value="150"

min={0}

step={1}

inputMode="numeric"

details="Current stock available for sale"

/>

<s-number-field

label="Discount percentage"

value="15"

suffix="%"

min={0}

max={100}

step={0.1}

inputMode="decimal"

/>

<s-number-field

label="Shipping weight"

value="2.5"

suffix="kg"

min={0.1}

step={0.1}

inputMode="decimal"

/>

</s-stack>

```html```

<s-stack gap="base">

<s-number-field

label="Inventory count"

value="150"

min="0"

step="1"

inputMode="numeric"

details="Current stock available for sale"

></s-number-field>

<s-number-field

label="Discount percentage"

value="15"

suffix="%"

min="0"

max="100"

step="0.1"

inputMode="decimal"

></s-number-field>

<s-number-field

label="Shipping weight"

value="2.5"

suffix="kg"

min="0.1"

step="0.1"

inputMode="decimal"

></s-number-field>

</s-stack>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)