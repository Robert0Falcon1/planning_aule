// Composable per gestire i colori delle aule

export function useAulaColor() {

  const colorMap = {
    'Aula Arancio': { bg: '#ff8c00', border: '#ff8c00' },
    'Aula Gialla': { bg: '#eaea00', border: '#eaea00' },
    'Aula Verde': { bg: '#28a745', border: '#28a745' },
    'Aula Azzurra': { bg: '#16d4f1', border: '#16d4f1' },
    'Aula Viola': { bg: '#9b59b6', border: '#9b59b6' },
    'Aula Mango': { bg: '#fcb500', border: '#22ca1a' },
    'Aula Lime': { bg: '#00ff04', border: '#00ff04' },
    'Aula Dragonfruit': { bg: '#ffffff', border: '#9e0242' },
    'Aula Cocco': { bg: '#6a3f14', border: '#2e221b' },
  }

  const defaultColors = { bg: '#6c757d', border: '#6c757d' }

  function getAulaColors(nomeAula) {
    if (!nomeAula) return defaultColors

    if (colorMap[nomeAula]) return colorMap[nomeAula]

    const matchingKey = Object.keys(colorMap).find(key =>
      nomeAula.toLowerCase().includes(key.toLowerCase())
    )

    return matchingKey ? colorMap[matchingKey] : defaultColors
  }

  function getAulaColor(nomeAula) {
    return getAulaColors(nomeAula).bg
  }

  function getAulaBorderColor(nomeAula) {
    return getAulaColors(nomeAula).border
  }

  function getAulaBadgeStyle(nomeAula) {
    const colors = getAulaColors(nomeAula)
    return {
      display: 'inline-block',
      width: '8px',
      height: '8px',
      borderRadius: '2px',
      backgroundColor: colors.bg,
      marginRight: '4px',
      verticalAlign: 'middle',
      flexShrink: 0,
    }
  }

  function getAulaBadgeStyle(nomeAula, borderWidth = '3px') {
    const colors = getAulaColors(nomeAula)
    return {
      display: 'inline-block',
      width: '12px',
      height: '12px',
      borderRadius: '2px',
      backgroundColor: colors.bg,
      border: `${borderWidth} solid ${colors.border}`,
      marginRight: '4px',
      verticalAlign: 'middle',
      flexShrink: 0,
    }
  }

  return {
    getAulaBadgeStyle,
    getAulaColor,
    getAulaBorderColor,
    getAulaColors,
  }
}