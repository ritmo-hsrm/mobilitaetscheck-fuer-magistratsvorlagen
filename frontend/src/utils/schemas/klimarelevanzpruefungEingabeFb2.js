import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  b1q1: number().required('Seite 1, Frage 1'),
  b1q2: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q3: string().when('b1q2', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q4: number().when('b1q3', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q5: string().when('b1q4', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q6: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 6'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q7: string().when('b1q6', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 7'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q8: number().when('b1q6', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 8'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q9: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 9'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q10: string().when('b1q9', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 10'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q11: string().when('b1q9', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 11'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q12: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 12'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q13: string().when('b1q12', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 13'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q14: string().when('b1q12', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 14'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q15: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 15'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q16: string().when('b1q15', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 16'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q17: string().when('b1q15', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 17'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q18: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 18'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q19: string().when('b1q18', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 19'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q20: string().when('b1q18', {
    is: 2,
    then: (schema) => schema.required('Seite 1, Frage 20'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q1: number().required('Seite 2, Frage 1'),
  b2q2: string().when('b2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q3: string().when('b2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q4: number().when('b2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q5: string().when('b2q4', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  })
})
