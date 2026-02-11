---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/choicelist",
    "fetched_at": "2026-02-10T13:29:38.761666",
    "status": 200,
    "size_bytes": 301897
  },
  "metadata": {
    "title": "ChoiceList",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "choicelist"
  }
}
---

# ChoiceList

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ChoiceListAsk assistantPresent multiple options to users, allowing either single selections with radio buttons or multiple selections with checkboxes.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties)Properties[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

`disabled` on any child choices is ignored when this is true.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to multiple](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-multiple)multiple**multiple**boolean**boolean**Default: false**Default: false**Whether multiple choices can be selected.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to values](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#properties-propertydetail-values)values**values**string[]**string[]**An array of the `value`s of the selected options.

This is a convenience prop for setting the `selected` prop on child options.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to choice](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#choice)ChoiceCreate options that let users select one or multiple items from a list of choices.

[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#choice-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label used for users using assistive technologies like screen readers. When set, any children or `label` supplied will not be announced. This can also be used to display a control without a visual label, while still providing context to users using screen readers.

[Anchor to defaultSelected](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#choice-propertydetail-defaultselected)defaultSelected**defaultSelected**boolean**boolean**Default: false**Default: false**Whether the control is active by default.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#choice-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the control, disallowing any interaction.

[Anchor to selected](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#choice-propertydetail-selected)selected**selected**boolean**boolean**Default: false**Default: false**Whether the control is active.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#choice-propertydetail-value)value**value**string**string**The value used in form data when the control is checked.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**Content to use as the choice label.

The label is produced by extracting and concatenating the text nodes from the provided content; any markup or element structure is ignored.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#slots-propertydetail-details)details**details**HTMLElement**HTMLElement**Additional text to provide context or guidance for the input.

This text is displayed along with the input and its label to offer more information or instructions to the user.

[Anchor to secondary-content](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#slots-propertydetail-secondarycontent)secondary-content**secondary-content**HTMLElement**HTMLElement**Additional content to display below the choice label. Can include rich content like TextFields, Buttons, or other interactive components. Event handlers on React components are preserved.

ExamplesCodejsxhtmlCopy9912345678910111213141516const handleChange = (event) => {  console.log('Values: ', event.currentTarget.values)}return (  <s-choice-list    label="Company name"    name="Company name"    details="The company name will be displayed on the checkout page."    onChange={handleChange}  >    <s-choice value="hidden">Hidden</s-choice>    <s-choice value="optional">Optional</s-choice>    <s-choice value="required">Required</s-choice>  </s-choice-list>)## Preview### Examples- #### Codejsx```

const handleChange = (event) => {

console.log('Values: ', event.currentTarget.values)

}

return (

<s-choice-list

label="Company name"

name="Company name"

details="The company name will be displayed on the checkout page."

onChange={handleChange}

>

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required">Required</s-choice>

</s-choice-list>

)

```html```

<script>

const handleChange = (event) =>

console.log('Values: ', event.currentTarget.values);

</script>

<s-choice-list

label="Company name"

name="Company name"

details="The company name will be displayed on the checkout page."

onChange="handleChange(event)"

>

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required">Required</s-choice>

</s-choice-list>

```- #### Basic usageDescriptionDemonstrates a basic ChoiceList with single selection, showing how to create a group of radio button choices.jsx```

<s-choice-list label="Product visibility" name="visibility">

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required" selected>

Required

</s-choice>

</s-choice-list>

```html```

<s-choice-list label="Product visibility" name="visibility">

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required" selected>Required</s-choice>

</s-choice-list>

```- #### Multiple selectionsDescriptionIllustrates a ChoiceList with multiple selection enabled, allowing users to choose multiple options with additional descriptive details for each choice.jsx```

<s-choice-list label="Checkout options" name="checkout" multiple>

<s-choice value="shipping" selected>

Use the shipping address as the billing address by default

<s-text slot="details">

Reduces the number of fields required to check out. The billing address

can still be edited.

</s-text>

</s-choice>

<s-choice value="confirmation">

Require a confirmation step

<s-text slot="details">

Customers must review their order details before purchasing.

</s-text>

</s-choice>

</s-choice-list>

```html```

<s-choice-list label="Checkout options" name="checkout" multiple>

<s-choice value="shipping" selected>

Use the shipping address as the billing address by default

<s-text slot="details">

Reduces the number of fields required to check out. The billing address

can still be edited.

</s-text>

</s-choice>

<s-choice value="confirmation">

Require a confirmation step

<s-text slot="details">

Customers must review their order details before purchasing.

</s-text>

</s-choice>

</s-choice-list>

```- #### With error stateDescriptionShows how to display an error message in a ChoiceList when an invalid selection is made or a validation constraint is not met.jsx```

<s-choice-list

label="Product visibility"

error="Please select an option"

>

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required">Required</s-choice>

</s-choice-list>

```html```

<s-choice-list

label="Product visibility"

name="visibility"

error="Product visibility cannot be hidden at this time"

>

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required" selected>Required</s-choice>

</s-choice-list>

```- #### Multiple choices with detailsDescriptionShowcases a multiple-selection ChoiceList with each option including detailed information.jsx```

<s-choice-list

label="Available shipping methods"

name="shipping-methods"

multiple

>

<s-choice value="standard" selected>

Standard shipping

<s-text slot="details">5-7 business days delivery</s-text>

</s-choice>

<s-choice value="express" selected>

Express shipping

<s-text slot="details">2-3 business days delivery</s-text>

</s-choice>

<s-choice value="overnight">

Overnight shipping

<s-text slot="details">Next business day delivery</s-text>

</s-choice>

</s-choice-list>

```html```

<s-choice-list

label="Available shipping methods"

name="shipping-methods"

multiple

>

<s-choice value="standard" selected>

Standard shipping

<s-text slot="details">5-7 business days delivery</s-text>

</s-choice>

<s-choice value="express" selected>

Express shipping

<s-text slot="details">2-3 business days delivery</s-text>

</s-choice>

<s-choice value="overnight">

Overnight shipping

<s-text slot="details">Next business day delivery</s-text>

</s-choice>

</s-choice-list>

```- #### Choice list validationDescriptionInteractive example showing required choice validation with dynamic error messages.jsx```

const [error, setError] = useState('Please select at least one option');

return (

<s-section>

<s-stack gap="base" justifyContent="start">

<s-choice-list

label="Product visibility"

name="visibility"

error={error}

onChange={(e) => {

setError(e.currentTarget.values.length > 0 ? '' : 'Please select at least one option');

}}

>

<s-choice value="hidden">Hidden</s-choice>

<s-choice value="optional">Optional</s-choice>

<s-choice value="required">Required</s-choice>

</s-choice-list>

</s-stack>

</s-section>

)

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#best-practices)Best practices

- Include a title that tells merchants what to do or explains the available options

- Label options clearly based on what the option will do

- Avoid mutually exclusive options when allowing multiple selection

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/forms/choicelist#content-guidelines)Content guidelines

- Write titles and choices in sentence case

- End titles with a colon if they introduce the list

- Start each choice with a capital letter

- Don't use commas or semicolons at the end of lines

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)