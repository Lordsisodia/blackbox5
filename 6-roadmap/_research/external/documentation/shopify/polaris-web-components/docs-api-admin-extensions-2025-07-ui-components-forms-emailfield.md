---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield",
    "fetched_at": "2026-02-10T13:28:39.830955",
    "status": 200,
    "size_bytes": 262286
  },
  "metadata": {
    "title": "EmailField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "emailfield"
  }
}
---

# EmailField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# EmailFieldAsk assistantUse this when you need users to provide their email addresses.

## [Anchor to emailfieldprops](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops)EmailFieldProps[Anchor to label](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-label)label**label**string**string**required**required**Content to use as the field label.

[Anchor to autocomplete](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-autocomplete)autocomplete**autocomplete**| AutocompleteField

| `${AutocompleteSectionAutocompleteSection} ${AutocompleteField}`

| `${AutocompleteGroupAutocompleteGroup} ${AutocompleteField}`

| `${AutocompleteSectionAutocompleteSection} ${AutocompleteGroupAutocompleteGroup} ${AutocompleteField}`

| boolean**| AutocompleteField

| `${AutocompleteSectionAutocompleteSection} ${AutocompleteField}`

| `${AutocompleteGroupAutocompleteGroup} ${AutocompleteField}`

| `${AutocompleteSectionAutocompleteSection} ${AutocompleteGroupAutocompleteGroup} ${AutocompleteField}`

| boolean**A hint as to the intended content of the field.

When set to `true`, this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `false`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-defaultvalue)defaultValue**defaultValue**string | string[]**string | string[]**A default value to populate for uncontrolled components.

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-disabled)disabled**disabled**boolean**boolean**Whether the field can be modified.

[Anchor to error](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-id)id**id**string**string**A unique identifier for the field.

[Anchor to maxLength](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-maxlength)maxLength**maxLength**number**number**Specifies the maximum number of characters allowed.

[Anchor to minLength](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-minlength)minLength**minLength**number**number**Specifies the min number of characters allowed.

[Anchor to name](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing `Form` component.

[Anchor to onBlur](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-onblur)onBlur**onBlur**() => void**() => void**Callback when focus is removed.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-onchange)onChange**onChange**(value: string) => void**(value: string) => void**Callback when the user has **finished editing** a field. Unlike `onChange` callbacks you may be familiar with from React component libraries, this callback is **not** run on every change to the input. Text fields are “partially controlled” components, which means that while the user edits the field, its state is controlled by the component. Once the user has signalled that they have finished editing the field (typically, by blurring the field), `onChange` is called if the input actually changed from the most recent `value` property. At that point, you are expected to store this “committed value” in state, and reflect it in the text field’s `value` property.

This state management model is important given how UI Extensions are rendered. UI Extension components run on a separate thread from the UI, so they can’t respond to input synchronously. A pattern popularized by [controlled React components](https://reactjs.org/docs/forms.html#controlled-components) is to have the component be the source of truth for the input `value`, and update the `value` on every user input. The delay in responding to events from a UI extension is only a few milliseconds, but attempting to strictly store state with this delay can cause issues if a user types quickly, or if the user is using a lower-powered device. Having the UI thread take ownership for “in progress” input, and only synchronizing when the user is finished with a field, avoids this risk.

It can still sometimes be useful to be notified when the user makes any input in the field. If you need this capability, you can use the `onInput` prop. However, never use that property to create tightly controlled state for the `value`.

This callback is called with the current value of the field. If the value of a field is the same as the current `value` prop provided to the field, the `onChange` callback will not be run.

[Anchor to onFocus](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-onfocus)onFocus**onFocus**() => void**() => void**Callback when input is focused.

[Anchor to onInput](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-oninput)onInput**onInput**(value: string) => void**(value: string) => void**Callback when the user makes any changes in the field. As noted in the documentation for `onChange`, you **must not** use this to update `value` — use the `onChange` callback for that purpose. Use the `onInput` prop when you need to do something as soon as the user makes a change, like clearing validation errors that apply to the field as soon as the user begins making the necessary adjustments.

This callback is called with the current value of the field.

[Anchor to placeholder](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Whether the field is read-only.

[Anchor to required](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-required)required**required**boolean**boolean**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` prop.

[Anchor to value](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#emailfieldprops-propertydetail-value)value**value**T**T**The current value for the field. If omitted, the field will be empty. You should update this value in response to the `onChange` callback.

### AutocompleteSectionThe “section” scopes the autocomplete data that should be inserted to a specific area of the page.

Commonly used when there are multiple fields with the same autocomplete needs in the same page. For example: 2 shipping address forms in the same page.```

`section-${string}`

```### AutocompleteGroupThe contact information group the autocomplete data should be sourced from.```

'shipping' | 'billing'

```ExamplesSimple EmailField exampleReactJSCopy91234567import {render, EmailField} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return <EmailField label="Enter your email address" />;}## Preview### Examples- #### Simple EmailField exampleReact```

import {render, EmailField} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return <EmailField label="Enter your email address" />;

}

```JS```

import {extend, EmailField} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const emailField = root.createComponent(EmailField, {

label: 'Enter your email address',

});

root.appendChild(emailField);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/forms/emailfield#related)Related[TextFieldTextField](/docs/api/admin-extensions/components/forms/textfield)[ - TextField](/docs/api/admin-extensions/components/forms/textfield)[NumberFieldNumberField](/docs/api/admin-extensions/components/forms/numberfield)[ - NumberField](/docs/api/admin-extensions/components/forms/numberfield)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)