import React, {useCallback} from 'react'
import Select from 'react-select'

import startupData from './startups.json'
const startups = startupData.data

const startupOptions = startups.filter(s => {
  return s.attributes.status !== 'death'
}).map(s => {
  s.value = s.id
  s.label = s.attributes.name
  return s
})

function StartupInput({ value, onChange }) {
  return (
    <div className="form__group">
        <label htmlFor="startup">Nom de la Startup d'État</label>
        <Select
        id="startup"
        onChange={onChange}
        placeholder='Mes Aides'
        options={startupOptions}
        />
    </div>
  )
}

export default StartupInput
