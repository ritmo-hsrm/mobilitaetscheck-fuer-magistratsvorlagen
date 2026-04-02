import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  d1q1: number().required('Seite 1, Frage 1'),
  d1q2: string().when('d1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  d2q1: number().required('Seite 2, Frage 1'),
  d2q2: string().when('d2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  })
})
