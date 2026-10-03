import { useState, useEffect } from 'react'
import { quizData, Question } from './data/quiz'

type GameState = 'start' | 'playing' | 'results'

function App() {
  const [gameState, setGameState] = useState<GameState>('start')
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [score, setScore] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showExplanation, setShowExplanation] = useState(false)
  const [answers, setAnswers] = useState<boolean[]>([])
  const [timeLeft, setTimeLeft] = useState(15)
  const [isAnswered, setIsAnswered] = useState(false)

  const question: Question = quizData[currentQuestion]
  const progress = ((currentQuestion + 1) / quizData.length) * 100

  useEffect(() => {
    if (gameState !== 'playing' || isAnswered) return

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          handleTimeUp()
          return 15
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [gameState, currentQuestion, isAnswered])

  const handleTimeUp = () => {
    if (!isAnswered) {
      setIsAnswered(true)
      setShowExplanation(true)
      setAnswers((prev) => [...prev, false])
    }
  }

  const startGame = () => {
    setGameState('playing')
    setCurrentQuestion(0)
    setScore(0)
    setSelectedAnswer(null)
    setShowExplanation(false)
    setAnswers([])
    setTimeLeft(15)
    setIsAnswered(false)
  }

  const handleAnswer = (index: number) => {
    if (isAnswered) return

    setSelectedAnswer(index)
    setIsAnswered(true)
    setShowExplanation(true)

    const isCorrect = index === question.correctAnswer
    if (isCorrect) {
      setScore((prev) => prev + 1)
    }
    setAnswers((prev) => [...prev, isCorrect])
  }

  const nextQuestion = () => {
    if (currentQuestion < quizData.length - 1) {
      setCurrentQuestion((prev) => prev + 1)
      setSelectedAnswer(null)
      setShowExplanation(false)
      setTimeLeft(15)
      setIsAnswered(false)
    } else {
      setGameState('results')
    }
  }

  const getOptionClass = (index: number) => {
    if (!showExplanation) {
      return selectedAnswer === index ? styles.selectedOption : styles.option
    }

    if (index === question.correctAnswer) {
      return styles.correctOption
    }

    if (selectedAnswer === index) {
      return styles.wrongOption
    }

    return styles.option
  }

  const getScoreMessage = () => {
    const percentage = (score / quizData.length) * 100
    if (percentage === 100) return 'Perfect Score! Amazing!'
    if (percentage >= 80) return 'Great Job! Well done!'
    if (percentage >= 60) return 'Good Effort! Keep learning!'
    if (percentage >= 40) return 'Not bad! Try again!'
    return 'Keep practicing! You can do better!'
  }

  if (gameState === 'start') {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.icon}>📝</div>
          <h1 style={styles.title}>Quiz Time!</h1>
          <p style={styles.description}>
            Test your knowledge with {quizData.length} questions. You have 15 seconds for each question.
          </p>
          <div style={styles.startInfo}>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Questions</span>
              <span style={styles.infoValue}>{quizData.length}</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Time per Question</span>
              <span style={styles.infoValue}>15s</span>
            </div>
          </div>
          <button onClick={startGame} style={styles.startButton}>
            Start Quiz
          </button>
        </div>
      </div>
    )
  }

  if (gameState === 'results') {
    const percentage = Math.round((score / quizData.length) * 100)
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.resultsIcon}>
            {percentage >= 60 ? '🎉' : '📚'}
          </div>
          <h1 style={styles.title}>Quiz Complete!</h1>
          <p style={styles.resultMessage}>{getScoreMessage()}</p>

          <div style={styles.scoreCircle}>
            <svg viewBox="0 0 100 100" style={styles.scoreSvg}>
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="8"
              />
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke={percentage >= 60 ? '#10b981' : '#ef4444'}
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${(percentage / 100) * 283} 283`}
                transform="rotate(-90 50 50)"
              />
            </svg>
            <div style={styles.scoreText}>
              <span style={styles.scoreNumber}>{percentage}%</span>
              <span style={styles.scoreLabel}>Score</span>
            </div>
          </div>

          <div style={styles.finalScore}>
            {score} out of {quizData.length} correct
          </div>

          <div style={styles.answersReview}>
            {answers.map((correct, index) => (
              <div
                key={index}
                style={{
                  ...styles.answerDot,
                  backgroundColor: correct ? '#10b981' : '#ef4444',
                }}
                title={`Question ${index + 1}: ${correct ? 'Correct' : 'Incorrect'}`}
              />
            ))}
          </div>

          <button onClick={startGame} style={styles.startButton}>
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.progressContainer}>
          <div style={styles.progressBar}>
            <div style={{ ...styles.progressFill, width: `${progress}%` }} />
          </div>
          <div style={styles.progressText}>
            Question {currentQuestion + 1} of {quizData.length}
          </div>
        </div>

        <div style={styles.timerContainer}>
          <div
            style={{
              ...styles.timer,
              backgroundColor: timeLeft <= 5 ? '#ef4444' : '#3b82f6',
            }}
          >
            {timeLeft}s
          </div>
        </div>

        <h2 style={styles.question}>{question.question}</h2>

        <div style={styles.options}>
          {question.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswer(index)}
              className={getOptionClass(index)}
              style={getOptionClass(index)}
              disabled={isAnswered}
            >
              <span style={styles.optionLetter}>
                {String.fromCharCode(65 + index)}
              </span>
              <span style={styles.optionText}>{option}</span>
            </button>
          ))}
        </div>

        {showExplanation && (
          <div style={styles.explanation}>
            <strong>Explanation:</strong> {question.explanation}
          </div>
        )}

        {showExplanation && (
          <button onClick={nextQuestion} style={styles.nextButton}>
            {currentQuestion < quizData.length - 1 ? 'Next Question' : 'See Results'}
          </button>
        )}
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
    padding: '20px',
  },
  card: {
    backgroundColor: '#16213e',
    borderRadius: '20px',
    padding: '32px',
    width: '100%',
    maxWidth: '600px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
  },
  icon: {
    fontSize: '64px',
    marginBottom: '16px',
    textAlign: 'center' as const,
  },
  title: {
    color: '#ffffff',
    fontSize: '32px',
    fontWeight: 700,
    textAlign: 'center' as const,
    marginBottom: '16px',
  },
  description: {
    color: '#94a3b8',
    fontSize: '16px',
    textAlign: 'center' as const,
    marginBottom: '24px',
  },
  startInfo: {
    display: 'flex',
    justifyContent: 'center',
    gap: '32px',
    marginBottom: '32px',
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
  },
  infoLabel: {
    color: '#64748b',
    fontSize: '12px',
    marginBottom: '4px',
  },
  infoValue: {
    color: '#ffffff',
    fontSize: '24px',
    fontWeight: 600,
  },
  startButton: {
    width: '100%',
    padding: '16px',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '12px',
    fontSize: '18px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  progressContainer: {
    marginBottom: '20px',
  },
  progressBar: {
    height: '8px',
    backgroundColor: '#0f3460',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '8px',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3b82f6',
    transition: 'width 0.3s',
  },
  progressText: {
    color: '#64748b',
    fontSize: '12px',
    textAlign: 'right' as const,
  },
  timerContainer: {
    display: 'flex',
    justifyContent: 'flex-end',
    marginBottom: '16px',
  },
  timer: {
    padding: '8px 16px',
    borderRadius: '8px',
    color: '#ffffff',
    fontSize: '14px',
    fontWeight: 600,
    transition: 'background-color 0.3s',
  },
  question: {
    color: '#ffffff',
    fontSize: '20px',
    fontWeight: 600,
    marginBottom: '24px',
    lineHeight: 1.5,
  },
  options: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
    marginBottom: '20px',
  },
  option: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    padding: '16px',
    backgroundColor: '#0f3460',
    border: '2px solid transparent',
    borderRadius: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    textAlign: 'left' as const,
  },
  selectedOption: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    padding: '16px',
    backgroundColor: '#1e3a5f',
    border: '2px solid #3b82f6',
    borderRadius: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    textAlign: 'left' as const,
  },
  correctOption: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    padding: '16px',
    backgroundColor: '#065f46',
    border: '2px solid #10b981',
    borderRadius: '12px',
    transition: 'all 0.2s',
    textAlign: 'left' as const,
  },
  wrongOption: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    padding: '16px',
    backgroundColor: '#7f1d1d',
    border: '2px solid #ef4444',
    borderRadius: '12px',
    transition: 'all 0.2s',
    textAlign: 'left' as const,
  },
  optionLetter: {
    width: '32px',
    height: '32px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#16213e',
    borderRadius: '8px',
    color: '#94a3b8',
    fontWeight: 600,
    flexShrink: 0,
  },
  optionText: {
    color: '#ffffff',
    fontSize: '16px',
    flex: 1,
  },
  explanation: {
    backgroundColor: '#0f3460',
    padding: '16px',
    borderRadius: '12px',
    color: '#94a3b8',
    fontSize: '14px',
    lineHeight: 1.6,
    marginBottom: '20px',
  },
  nextButton: {
    width: '100%',
    padding: '16px',
    backgroundColor: '#10b981',
    color: '#ffffff',
    border: 'none',
    borderRadius: '12px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  resultsIcon: {
    fontSize: '80px',
    marginBottom: '16px',
    textAlign: 'center' as const,
  },
  resultMessage: {
    color: '#94a3b8',
    fontSize: '18px',
    textAlign: 'center' as const,
    marginBottom: '32px',
  },
  scoreCircle: {
    position: 'relative',
    width: '160px',
    height: '160px',
    margin: '0 auto 24px',
  },
  scoreSvg: {
    width: '100%',
    height: '100%',
  },
  scoreText: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    textAlign: 'center' as const,
  },
  scoreNumber: {
    display: 'block',
    color: '#ffffff',
    fontSize: '36px',
    fontWeight: 700,
  },
  scoreLabel: {
    display: 'block',
    color: '#64748b',
    fontSize: '14px',
  },
  finalScore: {
    color: '#94a3b8',
    fontSize: '18px',
    textAlign: 'center' as const,
    marginBottom: '24px',
  },
  answersReview: {
    display: 'flex',
    justifyContent: 'center',
    gap: '8px',
    marginBottom: '32px',
  },
  answerDot: {
    width: '24px',
    height: '24px',
    borderRadius: '50%',
  },
}

export default App
