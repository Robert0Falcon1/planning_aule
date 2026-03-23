// Composable per gestire i colori delle aule

export function useAulaColor() {

  const colorMap = {
    'Aula Arancio': '#ff8c00',
    'Aula Gialla':  '#ffd700',
    'Aula Verde':   '#28a745',
    'Aula Azzurra': '#17a2b8',
    'Aula Viola':   '#9b59b6',
  }

  const defaultColor = '#6c757d'


  function getAulaColor(nomeAula) {
    if (!nomeAula) return defaultColor
    
    if (colorMap[nomeAula]) return colorMap[nomeAula]
    
    const matchingKey = Object.keys(colorMap).find(key => 
      nomeAula.toLowerCase().includes(key.toLowerCase())
    )
    
    return matchingKey ? colorMap[matchingKey] : defaultColor
  }

  function getAulaBadgeStyle(nomeAula) {
    return {
      display: 'inline-block',
      width: '8px',
      height: '8px',
      borderRadius: '2px',
      backgroundColor: getAulaColor(nomeAula),
      marginRight: '4px',
      verticalAlign: 'middle',
      flexShrink: 0,
    }
  }

  return {
    getAulaBadgeStyle,
    getAulaColor,
  }
}