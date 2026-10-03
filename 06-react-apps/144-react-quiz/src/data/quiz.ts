export interface Question {
  id: number
  question: string
  options: string[]
  correctAnswer: number
  explanation: string
}

export const quizData: Question[] = [
  {
    id: 1,
    question: 'What is the capital of France?',
    options: ['London', 'Berlin', 'Paris', 'Madrid'],
    correctAnswer: 2,
    explanation: 'Paris is the capital and largest city of France.',
  },
  {
    id: 2,
    question: 'Which planet is known as the Red Planet?',
    options: ['Venus', 'Mars', 'Jupiter', 'Saturn'],
    correctAnswer: 1,
    explanation: 'Mars is called the Red Planet due to its reddish appearance.',
  },
  {
    id: 3,
    question: 'What is the largest mammal on Earth?',
    options: ['Elephant', 'Blue Whale', 'Giraffe', 'Shark'],
    correctAnswer: 1,
    explanation: 'The Blue Whale is the largest mammal and the largest animal ever known to have existed.',
  },
  {
    id: 4,
    question: 'Who painted the Mona Lisa?',
    options: ['Michelangelo', 'Leonardo da Vinci', 'Raphael', 'Donatello'],
    correctAnswer: 1,
    explanation: 'Leonardo da Vinci painted the Mona Lisa between 1503 and 1519.',
  },
  {
    id: 5,
    question: 'What is the chemical symbol for gold?',
    options: ['Go', 'Gd', 'Au', 'Ag'],
    correctAnswer: 2,
    explanation: 'Au comes from the Latin word "aurum" meaning gold.',
  },
  {
    id: 6,
    question: 'Which country has the largest population?',
    options: ['United States', 'India', 'China', 'Indonesia'],
    correctAnswer: 2,
    explanation: 'China has been the most populous country, though India has recently surpassed it.',
  },
  {
    id: 7,
    question: 'What year did World War II end?',
    options: ['1943', '1944', '1945', '1946'],
    correctAnswer: 2,
    explanation: 'World War II ended in 1945 with the surrender of Japan.',
  },
  {
    id: 8,
    question: 'What is the smallest prime number?',
    options: ['0', '1', '2', '3'],
    correctAnswer: 2,
    explanation: '2 is the smallest and only even prime number.',
  },
  {
    id: 9,
    question: 'Which element has the atomic number 1?',
    options: ['Helium', 'Hydrogen', 'Oxygen', 'Carbon'],
    correctAnswer: 1,
    explanation: 'Hydrogen has atomic number 1, meaning it has one proton.',
  },
  {
    id: 10,
    question: 'What is the largest ocean on Earth?',
    options: ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'],
    correctAnswer: 3,
    explanation: 'The Pacific Ocean is the largest and deepest ocean on Earth.',
  },
]
