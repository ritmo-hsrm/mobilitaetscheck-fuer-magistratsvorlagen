import { object, string, number } from 'yup'

// Validation schema
export const schema = object({
  name: string().required('Angabe ist erforderlich'),
  zielSetId: number().nullable().optional().integer()
})
