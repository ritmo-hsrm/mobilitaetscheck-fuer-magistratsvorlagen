import * as yup from 'yup'

export const schema = yup.object({
  email: yup.string().email('Ungültige E-Mail-Adresse').nullable().label('E-Mail'),
  vorname: yup.string().required('Vorname ist erforderlich').label('Vorname'),
  nachname: yup.string().required('Nachname ist erforderlich').label('Nachname'),
  gruppeId: yup.number().nullable().label('Gruppe'),
})
