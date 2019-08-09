import React, {useCallback} from 'react'
import Select from 'react-select'

function StartupInput({ options, value, onChange }) {
  return (
    <div className="form__group">
        <label htmlFor="startup">Nom de la Startup d'État</label>
        <Select
        id="startup"
        onChange={onChange}
        placeholder='Mes Aides'
        options={options}
        />
    </div>
  )
}

export default StartupInput
