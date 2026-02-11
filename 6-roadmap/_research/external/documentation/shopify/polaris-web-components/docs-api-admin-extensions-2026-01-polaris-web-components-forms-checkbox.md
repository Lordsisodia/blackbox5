---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/checkbox",
    "fetched_at": "2026-02-10T13:29:36.883850",
    "status": 200,
    "size_bytes": 282952
  },
  "metadata": {
    "title": "Checkbox",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "checkbox"
  }
}
---

# Checkbox

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# CheckboxAsk assistantGive users a clear way to make selections, such as agreeing to terms or choosing multiple items from a list.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label used for users using assistive technologies like screen readers. When set, any children or `label` supplied will not be announced. This can also be used to display a control without a visual label, while still providing context to users using screen readers.

[Anchor to checked](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-checked)checked**checked**boolean**boolean**Default: false**Default: false**Whether the control is active.

[Anchor to defaultChecked](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-defaultchecked)defaultChecked**defaultChecked**boolean**boolean**Default: false**Default: false**Whether the control is active by default.

[Anchor to defaultIndeterminate](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-defaultindeterminate)defaultIndeterminate**defaultIndeterminate**boolean**boolean**Default: false**Default: false**[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to indeterminate](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-indeterminate)indeterminate**indeterminate**boolean**boolean**[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-label)label**label**string**string**Visual content to use as the control label.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#properties-propertydetail-value)value**value**string**string**The value used in form data when the checkbox is checked.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91234<s-checkbox  label="Require a confirmation step"  details="Ensure all criteria are met before proceeding" />## Preview### Examples- #### Codejsx```

<s-checkbox

label="Require a confirmation step"

details="Ensure all criteria are met before proceeding"

/>

```html```

<s-checkbox

label="Require a confirmation step"

details="Ensure all criteria are met before proceeding"

></s-checkbox>

```- #### Indeterminate stateDescriptionCheckbox in indeterminate state, commonly used for "select all" functionality when some items are selected.jsx```

const [selectedItems, setSelectedItems] = useState([]);

const items = ['Item 1', 'Item 2', 'Item 3'];

const toggleItem = (value, checked) => setSelectedItems(checked ? [...selectedItems, value] : selectedItems.filter(item => item !== value));

const toggleAll = (checked) => setSelectedItems(checked ? items : []);

const isSelected = (item) => selectedItems.includes(item);

return (

<s-stack gap="small">

<s-checkbox

label="Select all items"

indeterminate={selectedItems.length !== 0 && selectedItems.length !== items.length}

checked={selectedItems.length === items.length}

onChange={e => toggleAll(e.currentTarget.checked)}

/>

<s-divider />

{items.map(i => (

<s-checkbox key={i} label={i} checked={isSelected(i)} onChange={e => toggleItem(i, e.currentTarget.checked)} />

))}

</s-stack>

);

```- #### Error stateDescriptionCheckbox with validation error message for required form fields.jsx```

<s-checkbox

label="I agree to the terms"

error="You must accept the terms to continue"

/>

```html```

<s-checkbox

label="I agree to the terms"

error="You must accept the terms to continue"

></s-checkbox>

```- #### Help textDescriptionCheckbox with descriptive details text to provide additional context about the option.jsx```

<s-checkbox

label="Send order notifications"

details="You'll receive emails when orders are placed, fulfilled, or cancelled"

/>

```html```

<s-checkbox

label="Send order notifications"

details="You'll receive emails when orders are placed, fulfilled, or cancelled"

></s-checkbox>

```- #### Disabled stateDescriptionCheckbox in disabled state with explanatory details about why it's unavailable.jsx```

<s-checkbox

label="Advanced settings"

disabled

details="Contact your administrator to enable advanced settings"

/>

```html```

<s-checkbox

label="Advanced settings"

disabled

details="Contact your administrator to enable advanced settings"

></s-checkbox>

```- #### Settings groupDescriptionMultiple checkboxes for different configuration options with helpful details.jsx```

<s-stack gap="base">

<s-checkbox label="Show only published products" checked />

<s-checkbox

label="Enable inventory tracking"

details="Track inventory levels and receive low stock alerts"

checked

/>

<s-checkbox

label="View customer data"

details="Allow staff to access customer contact information and order history"

/>

</s-stack>

```html```

<s-stack gap="base">

<s-checkbox label="Show only published products" checked></s-checkbox>

<s-checkbox

label="Enable inventory tracking"

details="Track inventory levels and receive low stock alerts"

checked

></s-checkbox>

<s-checkbox

label="View customer data"

details="Allow staff to access customer contact information and order history"

></s-checkbox>

</s-stack>

```- #### Checkbox validationDescriptionInteractive example showing required checkbox validation with dynamic error messages.jsx```

const [checked, setChecked] = useState(false);

const errorMessage = 'You must accept the terms to continue';

const [error, setError] = useState(errorMessage);

return (

<s-section>

<s-stack gap="base" justifyContent="start">

<s-text-field label="Name" />

<s-checkbox

label="I agree to the terms"

checked={checked}

error={error}

onChange={(e) => {

setChecked(e.currentTarget.checked);

setError(e.currentTarget.checked ? '' : errorMessage);

}}

/>

</s-stack>

</s-section>

)

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#best-practices)Best practices

- Use ChoiceList when rendering multiple checkboxes to provide a consistent and accessible selection interface

- Work independently from each other

- Be framed positively (e.g., "Publish store" not "Hide store")

- Always have a label when used to activate or deactivate a setting

- Be listed in a logical order (alphabetical, numerical, time-based, etc.)

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/forms/checkbox#content-guidelines)Content guidelines

- Start each option with a capital letter

- Don't use commas or semicolons at the end of each line

- Use first person when asking merchants to agree to terms (e.g., "I agree to the Terms of Service")

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)