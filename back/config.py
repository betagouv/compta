dtype = {
  'N° EJ': int
}

configs = {
  'P352': {
    'skiprows': 4,
    'columns': [
      'Centre financier',
      'Centre financier 2',
      'N° EJ',
      'Type de flux',
      'Fournisseur titulaire principal (EJ)',
      'N° de contrat',
      'N° poste EJ',
      'Centre de coûts',
      'Centre de coûts 2',
      'Fonds',
      'Fonds 2',
      'Compte budgétaire',
      'Compte budgétaire 2',
      'Référentiel de programmation',
      'Référentiel de programmation 2',
      'Groupe de marchandises',
      'Groupe de marchandises 2',
      'Date comptable du SF',
      'Bascule des EJ non soldés',
      'Montant engagé',
      'Montant certifié non soldé',
      'Montant pré-enregistré',
      'Montant facturé',
      'Montant payé',
    ],
    'exclusions': [
      1404742600 # Etalab AERIAL
    ]
  },
  'DG': {
    'skiprows': 4,
    'columns': [
      'Service exécutant',
      'Service exécutant 2',
      'Centre financier',
      'Centre financier 2',
      'N° EJ',
      'Type de flux',
      'Fournisseur titulaire principal (EJ)',
      'N° de contrat',
      'N° poste EJ',
      'Centre de coûts',
      'Centre de coûts 2',
      'Fonds',
      'Fonds 2',
      'Compte budgétaire',
      'Compte budgétaire 2',
      'Référentiel de programmation',
      'Référentiel de programmation 2',
      'Groupe de marchandises', 
      'Groupe de marchandises 2',
      'Date comptable du SF',
      'Bascule des EJ non soldés',
      'Montant engagé',
      'Montant certifié non soldé',
      'Montant pré-enregistré',
      'Montant facturé',
      'Montant payé',
    ],
    'exclusions': [
      1404486171, # Programme SIRH
      1404669643, # Programme SIRH
      1404738907, # Gouv.maîtrise risq.
    ]
  }
}
