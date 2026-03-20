import { array, number, object, string, date } from 'yup'
import { parseDate } from '@/utils/validation'

// Validation schema
export const schema = object({
  verwaltungsvorgangNr: string().required('Angabe ist erforderlich'),
  verwaltungsvorgangDatum: date().transform(parseDate).nullable().optional(),
  name: string().required('Angabe ist erforderlich'),
  beschreibung: string().nullable().optional(),
  gemeindeGebietIds: array().of(number()).nullable(true),
  tagIds: array().of(number()).nullable(true)
})
