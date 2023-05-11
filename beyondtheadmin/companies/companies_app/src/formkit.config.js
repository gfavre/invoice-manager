import { generateClasses } from '@formkit/themes'


const config = {
  config: {
    classes: generateClasses({
      global: { // classes
        outer: '$reset mb-3',
        input: 'form-control',
        label: 'form-label',
        help: 'form-text'
      },
      form: {
        form: "col-md-4 col-lg-3 mt-5 mx-auto p-5 border rounded"
      },
      file: {
        fileList: 'list-unstyled',
        input: 'custom-file-input',
        inner: 'custom-file',
      },
      range: {
        input: '$reset form-range',
      },
      submit: {
        outer: '$reset mt-3',
        input: '$reset btn btn-primary'
      }
    })
  },
}
export default config
