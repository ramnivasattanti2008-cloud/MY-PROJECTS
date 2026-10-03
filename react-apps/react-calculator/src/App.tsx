import { useState, useEffect, useCallback } from 'react'

type Operator = '+' | '-' | '*' | '/' | '='

interface CalcState {
  display: string
  previousValue: string | null
  operator: Operator | null
  waitingForOperand: boolean
}

function App() {
  const [state, setState] = useState<CalcState>({
    display: '0',
    previousValue: null,
    operator: null,
    waitingForOperand: false,
  })

  const clearAll = useCallback(() => {
    setState({
      display: '0',
      previousValue: null,
      operator: null,
      waitingForOperand: false,
    })
  }, [])

  const inputDigit = useCallback((digit: string) => {
    setState((prev) => {
      if (prev.waitingForOperand) {
        return {
          ...prev,
          display: digit,
          waitingForOperand: false,
        }
      }
      return {
        ...prev,
        display: prev.display === '0' ? digit : prev.display + digit,
      }
    })
  }, [])

  const inputDecimal = useCallback(() => {
    setState((prev) => {
      if (prev.waitingForOperand) {
        return {
          ...prev,
          display: '0.',
          waitingForOperand: false,
        }
      }
      if (prev.display.includes('.')) return prev
      return {
        ...prev,
        display: prev.display + '.',
      }
    })
  }, [])

  const performOperation = useCallback((nextOperator: Operator) => {
    const inputValue = parseFloat(state.display)

    if (state.operator && !state.waitingForOperand) {
      const prevValue = parseFloat(state.previousValue || '0')
      let result: number

      switch (state.operator) {
        case '+':
          result = prevValue + inputValue
          break
        case '-':
          result = prevValue - inputValue
          break
        case '*':
          result = prevValue * inputValue
          break
        case '/':
          result = inputValue === 0 ? 0 : prevValue / inputValue
          break
        default:
          result = inputValue
      }

      const newDisplay = String(result)

      if (nextOperator === '=') {
        setState({
          display: newDisplay,
          previousValue: null,
          operator: null,
          waitingForOperand: true,
        })
      } else {
        setState({
          display: newDisplay,
          previousValue: newDisplay,
          operator: nextOperator,
          waitingForOperand: true,
        })
      }
    } else {
      setState((prev) => ({
        ...prev,
        previousValue: String(inputValue),
        operator: nextOperator,
        waitingForOperand: true,
      }))
    }
  }, [state.display, state.operator, state.waitingForOperand, state.previousValue])

  const toggleSign = useCallback(() => {
    setState((prev) => ({
      ...prev,
      display: String(parseFloat(prev.display) * -1),
    }))
  }, [])

  const percentage = useCallback(() => {
    setState((prev) => ({
      ...prev,
      display: String(parseFloat(prev.display) / 100),
    }))
  }, [])

  const backspace = useCallback(() => {
    setState((prev) => {
      if (prev.waitingForOperand) return prev
      const newDisplay = prev.display.slice(0, -1)
      return {
        ...prev,
        display: newDisplay.length === 0 ? '0' : newDisplay,
      }
    })
  }, [])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const key = e.key

      if (key >= '0' && key <= '9') {
        inputDigit(key)
      } else if (key === '.') {
        inputDecimal()
      } else if (key === '+') {
        performOperation('+')
      } else if (key === '-') {
        performOperation('-')
      } else if (key === '*') {
        performOperation('*')
      } else if (key === '/') {
        e.preventDefault()
        performOperation('/')
      } else if (key === 'Enter' || key === '=') {
        performOperation('=')
      } else if (key === 'Escape') {
        clearAll()
      } else if (key === 'Backspace') {
        backspace()
      } else if (key === '%') {
        percentage()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [inputDigit, inputDecimal, performOperation, clearAll, backspace, percentage])

  const buttons = [
    { label: 'C', action: clearAll, className: 'function' },
    { label: '+/-', action: toggleSign, className: 'function' },
    { label: '%', action: percentage, className: 'function' },
    { label: '/', action: () => performOperation('/'), className: 'operator' },
    { label: '7', action: () => inputDigit('7'), className: 'number' },
    { label: '8', action: () => inputDigit('8'), className: 'number' },
    { label: '9', action: () => inputDigit('9'), className: 'number' },
    { label: '*', action: () => performOperation('*'), className: 'operator' },
    { label: '4', action: () => inputDigit('4'), className: 'number' },
    { label: '5', action: () => inputDigit('5'), className: 'number' },
    { label: '6', action: () => inputDigit('6'), className: 'number' },
    { label: '-', action: () => performOperation('-'), className: 'operator' },
    { label: '1', action: () => inputDigit('1'), className: 'number' },
    { label: '2', action: () => inputDigit('2'), className: 'number' },
    { label: '3', action: () => inputDigit('3'), className: 'number' },
    { label: '+', action: () => performOperation('+'), className: 'operator' },
    { label: '0', action: () => inputDigit('0'), className: 'number zero' },
    { label: '.', action: inputDecimal, className: 'number' },
    { label: '=', action: () => performOperation('='), className: 'operator' },
  ]

  return (
    <div style={styles.container}>
      <div style={styles.calculator}>
        <div style={styles.display}>
          <div style={styles.previousValue}>
            {state.previousValue} {state.operator || ''}
          </div>
          <div style={styles.currentValue}>{state.display}</div>
        </div>
        <div style={styles.buttonGrid}>
          {buttons.map((btn, index) => (
            <button
              key={index}
              onClick={btn.action}
              style={{ ...styles.button, ...styles[btn.className as keyof typeof styles] }}
            >
              {btn.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#1a1a2e',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  },
  calculator: {
    width: '320px',
    backgroundColor: '#16213e',
    borderRadius: '16px',
    padding: '20px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
  },
  display: {
    backgroundColor: '#0f3460',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '16px',
    textAlign: 'right' as const,
  },
  previousValue: {
    color: '#94a3b8',
    fontSize: '14px',
    height: '20px',
  },
  currentValue: {
    color: '#ffffff',
    fontSize: '36px',
    fontWeight: 600,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  buttonGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '10px',
  },
  button: {
    height: '60px',
    border: 'none',
    borderRadius: '12px',
    fontSize: '20px',
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'transform 0.1s, opacity 0.1s',
  },
  function: {
    backgroundColor: '#4a5568',
    color: '#ffffff',
  },
  operator: {
    backgroundColor: '#e94560',
    color: '#ffffff',
  },
  number: {
    backgroundColor: '#2d3748',
    color: '#ffffff',
  },
}

export default App
