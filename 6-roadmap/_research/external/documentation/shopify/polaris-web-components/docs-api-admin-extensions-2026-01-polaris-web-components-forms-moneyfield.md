---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/moneyfield",
    "fetched_at": "2026-02-10T13:29:58.259580",
    "status": 200,
    "size_bytes": 286967
  },
  "metadata": {
    "title": "MoneyField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "moneyfield"
  }
}
---

# MoneyField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# MoneyFieldAsk assistantCollect monetary values from users with built-in currency formatting and validation.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties)Properties[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-autocomplete)autocomplete**autocomplete**string**string**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to max](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-max)max**max**number**number**Default: Infinity**Default: Infinity**The highest decimal or integer to be accepted for the field. When used with `step` the value will round down to the max number.

Note: a user will still be able to use the keyboard to input a number higher than the max. It is up to the developer to add appropriate validation.

[Anchor to min](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-min)min**min**number**number**Default: -Infinity**Default: -Infinity**The lowest decimal or integer to be accepted for the field. When used with `step` the value will round up to the min number.

Note: a user will still be able to use the keyboard to input a number lower than the min. It is up to the developer to add appropriate validation.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/moneyfield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy912345<s-money-field  label="Regional Price"  placeholder="99.99"  details="Recommended price for the European market" />## Preview### Examples- #### Codejsx```

<s-money-field

label="Regional Price"

placeholder="99.99"

details="Recommended price for the European market"

/>

```html```

<s-money-field

label="Regional Price"

placeholder="99.99"

details="Recommended price for the European market"

></s-money-field>

```- #### Basic usageDescriptionDemonstrates a simple money field with a label, initial value, and numeric constraints.jsx```

<s-money-field

label="Price"

value="19.99"

min={0}

max={1000}

/>

```html```

<s-money-field

label="Price"

value="19.99"

min="0"

max="1000"

></s-money-field>

```- #### With validation limitsDescriptionShowcases a money field with explicit minimum and maximum value limits, and a detailed description for user guidance.jsx```

<s-money-field

label="Discount amount"

value="5.00"

min={0}

max={100}

details="Enter discount amount between $0 and $100"

/>

```html```

<s-money-field

label="Discount amount"

value="5.00"

min="0"

max="100"

details="Enter discount amount between $0 and $100"

></s-money-field>

```- #### Basic fieldDescriptionIllustrates a money field demonstrating basic error handling and validation.jsx```

<s-money-field

label="Product cost"

value="29.99"

min={0.01}

error="Product cost is required"

/>

```html```

<s-money-field

label="Product cost"

value="29.99"

min="0.01"

error="Product cost is required"

></s-money-field>

```- #### Currency formatting with form integrationDescriptionDisplays multiple money fields in a vertical stack, showing how to integrate multiple currency inputs in a form with varied details and constraints.jsx```

<s-stack direction="block" gap="base">

<s-money-field

label="Price"

value="0.00"

min={0.01}

max={99999.99}

details="Customers will see this price"

/>

<s-money-field

label="Compare at price"

value=""

min={0}

max={99999.99}

details="Show customers the original price when on sale"

/>

<s-money-field

label="Cost per item"

value=""

min={0}

max={99999.99}

details="Customers won't see this"

/>

</s-stack>

```html```

<s-stack direction="block" gap="base">

<s-money-field

label="Price"

value="0.00"

min="0.01"

max="99999.99"

details="Customers will see this price"

></s-money-field>

<s-money-field

label="Compare at price"

value=""

min="0"

max="99999.99"

details="Show customers the original price when on sale"

></s-money-field>

<s-money-field

label="Cost per item"

value=""

min="0"

max="99999.99"

details="Customers won't see this"

></s-money-field>

</s-stack>

```- #### Money field validationDescriptionInteractive example showing real-time validation with min/max limits and dynamic error messages.jsx```

const [amount, setAmount] = useState('150');

const [error, setError] = useState('Value must be no more than $100');

return (

<s-section>

<s-stack gap="base" justifyContent="start">

<s-text-field label="Product name" />

<s-money-field

label="Discount amount"

value={amount}

min={0}

max={100}

details="Enter discount amount between $0 and $100"

error={error}

onInput={(e) => {

setAmount(e.currentTarget.value);

const val = parseFloat(e.currentTarget.value);

setError(val > e.currentTarget.max ? 'Value must be no more than $100' : val < e.currentTarget.min ? 'Value must be at least $0' : '');

}}

/>

</s-stack>

</s-section>

)

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)