import { string, object } from 'yup'

// Validation schema
export const schema = object({
  d1q1: string().required('Seite 1, Frage 1'),
  d2q1: string().required('Seite 2, Frage 1')
})
