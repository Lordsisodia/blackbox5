---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/functionsettings",
    "fetched_at": "2026-02-10T13:28:42.460196",
    "status": 200,
    "size_bytes": 258393
  },
  "metadata": {
    "title": "FunctionSettings",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "functionsettings"
  }
}
---

# FunctionSettings

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# FunctionSettingsAsk assistantFunctionSettings should be used when configuring the metafield configuration of a Shopify Function. It provides a structure for various input fields and controls, such as text fields, checkboxes, and selections. It also integrates with the native Contextual Save Bar to handle form submission and reset actions.

## [Anchor to functionsettingsprops](/docs/api/admin-extensions/2025-07/ui-components/forms/functionsettings#functionsettingsprops)FunctionSettingsProps[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/functionsettings#functionsettingsprops-propertydetail-id)id**id**string**string**A unique identifier for the form.

[Anchor to onError](/docs/api/admin-extensions/2025-07/ui-components/forms/functionsettings#functionsettingsprops-propertydetail-onerror)onError**onError**(errors: FunctionSettingsErrorFunctionSettingsError[]) => void**(errors: FunctionSettingsErrorFunctionSettingsError[]) => void**An optional callback function that will be run by the admin when the committing the changes to Shopify’s servers fails. The errors you receive in the `errors` argument will only be those that were caused by data your extension provided; network errors and user errors that are out of your control will not be reported here.

In the `onError` callback, you should update your extension’s UI to highlight the fields that caused the errors, and display the error messages to the user.

[Anchor to onSave](/docs/api/admin-extensions/2025-07/ui-components/forms/functionsettings#functionsettingsprops-propertydetail-onsave)onSave**onSave**() => void | Promise<void>**() => void | Promise<void>**An optional callback function that will be run by the admin when the user commits their changes in the admin-rendered part of the function settings experience. If this function returns a promise, the admin will wait for the promise to resolve before committing any changes to Shopify’s servers. If the promise rejects, the admin will abort the changes and display an error, using the `message` property of the error you reject with.

### FunctionSettingsError- codeA unique identifier describing the “class” of error. These will match the GraphQL error codes as closely as possible. For example the enums returned by the `metafieldsSet` mutation```

string

```- messageA translated message describing the error.```

string

``````

export interface FunctionSettingsError {

/**

* A unique identifier describing the “class” of error. These will match

* the GraphQL error codes as closely as possible. For example the enums

* returned by the `metafieldsSet` mutation

*

* @see /docs/api/admin-graphql/latest/enums/MetafieldsSetUserErrorCode

*/

code: string;

/**

* A translated message describing the error.

*/

message: string;

}

```ExamplesSimple function settings form implementationReactJSCopy9912345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455import {  reactExtension,  useApi,  FunctionSettings,  TextField,  Section,} from '@shopify/ui-extensions-react/admin';export default reactExtension(  'admin.settings.validation.render',  async (api) => {    // Use Direct API access to fetch initial    // metafields from the server if we are    // rendering against a pre-existing `Validation`    const initialSettings = api.data.validation      ? await fetchSettings(api.data.validation.id)      : {};    return <App settings={initialSettings} />;});function App({settings}) {  const [value, setValue] = useState(settings);  const [error, setError] = useState();  const {applyMetafieldsChange} = useApi();  return (    <FunctionSettings      onError={(errors) => {        setError(errors[0]?.message);      }}    >      <Section heading="Settings">        <TextField          label="Name"          name="name"          value={value}          error={error}          onChange={(value) => {            setValue(value);            setError(undefined);            applyMetafieldsChange({              type: 'updateMetafield',              namespace: '$app:my_namespace',              key: 'name',              value,              valueType: 'single_line_text_field',            });          }}        />      </Section>    </FunctionSettings>  );}## Preview### Examples- #### Simple function settings form implementationReact```

import {

reactExtension,

useApi,

FunctionSettings,

TextField,

Section,

} from '@shopify/ui-extensions-react/admin';

export default reactExtension(

'admin.settings.validation.render',

async (api) => {

// Use Direct API access to fetch initial

// metafields from the server if we are

// rendering against a pre-existing `Validation`

const initialSettings = api.data.validation

? await fetchSettings(api.data.validation.id)

: {};

return <App settings={initialSettings} />;

});

function App({settings}) {

const [value, setValue] = useState(settings);

const [error, setError] = useState();

const {applyMetafieldsChange} = useApi();

return (

<FunctionSettings

onError={(errors) => {

setError(errors[0]?.message);

}}

>

<Section heading="Settings">

<TextField

label="Name"

name="name"

value={value}

error={error}

onChange={(value) => {

setValue(value);

setError(undefined);

applyMetafieldsChange({

type: 'updateMetafield',

namespace: '$app:my_namespace',

key: 'name',

value,

valueType: 'single_line_text_field',

});

}}

/>

</Section>

</FunctionSettings>

);

}

```JS```

import {

extension,

FunctionSettings,

TextField,

Section,

} from '@shopify/ui-extensions/admin';

export default extension(

'admin.settings.validation.render',

async (root, api) => {

// Use Direct API access to fetch initial

// metafields from the server if we are

// rendering against a pre-existing `Validation`

const initialSettings = api.data.validation

? await fetchSettings(api.data.validation.id)

: {};

const textField = root.createComponent(TextField, {

value: initialSettings.name,

label: 'Name',

name: 'name',

onChange(value) {

textField.updateProps({value, error: undefined});

api.applyMetafieldsChange({

type: 'updateMetafield',

namespace: '$app:my_namespace',

key: 'name',

value,

valueType: 'single_line_text_field',

});

},

});

const section = root.createComponent(Section, {

heading: 'Settings',

});

const settings = root.createComponent(FunctionSettings, {

onError(errors) {

textField.updateProps({error: errors[0]?.message});

},

});

section.append(textField);

settings.append(section);

},

);

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/forms/functionsettings#related)Related[TextFieldTextField](/docs/api/admin-extensions/components/forms/textfield)[ - TextField](/docs/api/admin-extensions/components/forms/textfield)[NumberFieldNumberField](/docs/api/admin-extensions/components/forms/numberfield)[ - NumberField](/docs/api/admin-extensions/components/forms/numberfield)[ChoiceListChoiceList](/docs/api/admin-extensions/components/forms/choicelist)[ - ChoiceList](/docs/api/admin-extensions/components/forms/choicelist)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)