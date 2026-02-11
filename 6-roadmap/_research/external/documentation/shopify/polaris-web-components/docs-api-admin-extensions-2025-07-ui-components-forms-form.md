---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/form",
    "fetched_at": "2026-02-10T13:28:41.153130",
    "status": 200,
    "size_bytes": 254302
  },
  "metadata": {
    "title": "Form",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "form"
  }
}
---

# Form

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# FormAsk assistantUse this component when you want to collect input from users. It provides a structure for various input fields and controls, such as text fields, checkboxes, and buttons. It also integrates with the native Contextual Save Bar to handle form submission and reset actions.

## [Anchor to formprops](/docs/api/admin-extensions/2025-07/ui-components/forms/form#formprops)FormProps[Anchor to onReset](/docs/api/admin-extensions/2025-07/ui-components/forms/form#formprops-propertydetail-onreset)onReset**onReset**() => void | Promise<void>**() => void | Promise<void>**required**required**A callback that is run when the form is reset.

[Anchor to onSubmit](/docs/api/admin-extensions/2025-07/ui-components/forms/form#formprops-propertydetail-onsubmit)onSubmit**onSubmit**() => void | Promise<void>**() => void | Promise<void>**required**required**A callback that is run when the form is submitted.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/form#formprops-propertydetail-id)id**id**string**string**A unique identifier for the form.

ExamplesSimple form implementationReactJSCopy99123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051import React, { useCallback, useState } from 'react';import {  reactExtension,  Form,  TextField,} from '@shopify/ui-extensions-react/admin';export default reactExtension("admin.product-details.block.render", () => <App />);function App() {  const [value, setValue] = useState("");  const [error, setError] = useState('');  const onSubmit = useCallback(    async () => {      // API call to save the values      const res = await fetch('/save', {method:'POST', body: JSON.stringify({name: value})});      if (!res.ok) {        const json = await res.json();        const errors = json.errors.join(',');        setError(errors);      }    },    [value]  );  const onReset = useCallback(async () => {     // Reset to initial value     setValue('')     // Clear errors     setError('')  }, []);  const onInput = useCallback((nameValue) => {    if (!nameValue) {      setError("Please enter a name.");    }  }, [])  // Field values can only be updated on change when using Remote UI.  const onChange = useCallback((nameValue) => {    setValue(nameValue);  }, [])  return (    <Form id="form" onSubmit={onSubmit} onReset={onReset}>      <TextField label="name" value={value} onInput={onInput} onChange={onChange} error={error} />    </Form>  );}## Preview### Examples- #### Simple form implementationReact```

import React, { useCallback, useState } from 'react';

import {

reactExtension,

Form,

TextField,

} from '@shopify/ui-extensions-react/admin';

export default reactExtension("admin.product-details.block.render", () => <App />);

function App() {

const [value, setValue] = useState("");

const [error, setError] = useState('');

const onSubmit = useCallback(

async () => {

// API call to save the values

const res = await fetch('/save', {method:'POST', body: JSON.stringify({name: value})});

if (!res.ok) {

const json = await res.json();

const errors = json.errors.join(',');

setError(errors);

}

},

[value]

);

const onReset = useCallback(async () => {

// Reset to initial value

setValue('')

// Clear errors

setError('')

}, []);

const onInput = useCallback((nameValue) => {

if (!nameValue) {

setError("Please enter a name.");

}

}, [])

// Field values can only be updated on change when using Remote UI.

const onChange = useCallback((nameValue) => {

setValue(nameValue);

}, [])

return (

<Form id="form" onSubmit={onSubmit} onReset={onReset}>

<TextField label="name" value={value} onInput={onInput} onChange={onChange} error={error} />

</Form>

);

}

```JS```

import {

extend,

Form,

TextField,

} from '@shopify/ui-extensions/admin';

extend('admin.product-details.block.render', (root) => {

let name = '';

const textField = root.createComponent(

TextField,

{

label: 'name',

value: name,

onChange: (value) => {

textField.updateProps({value});

name = value;

},

}

);

const onSubmit = async () => {

// API call to save the values

const res = await fetch('/save', {method:'POST', body: JSON.stringify({name})});

if (!res.ok) {

const json = await res.json();

// The Host can catch these errors and do something with them.

throw Error(`There were errors: ${json.errors.join(',')}`);

}

};

const onReset = async () => {

name = '';

};

const form = root.createComponent(

Form,

{onSubmit, onReset}

);

form.appendChild(textField);

root.appendChild(form);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/forms/form#related)Related[TextFieldTextField](/docs/api/admin-extensions/components/forms/textfield)[ - TextField](/docs/api/admin-extensions/components/forms/textfield)[NumberFieldNumberField](/docs/api/admin-extensions/components/forms/numberfield)[ - NumberField](/docs/api/admin-extensions/components/forms/numberfield)[EmailFieldEmailField](/docs/api/admin-extensions/components/forms/emailfield)[ - EmailField](/docs/api/admin-extensions/components/forms/emailfield)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)