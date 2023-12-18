import Foundation

class MorseCodeGenerator {
    let dotThreshold = 80
    let dashThreshold = 90
    let interferenceThreshold = 250
    let characterPauseThreshold = 500
    let unitTime = 5
    var currentSignal: Int? = nil
    var duration = 0

    func send(signal: Int) -> String? {
        if signal == currentSignal {
            duration += unitTime
            return nil
        } else {
            var result: String? = nil
            if let currentSignal = currentSignal {
                if currentSignal == 1 {
                    if duration <= dotThreshold {
                        result = "."
                    } else if duration >= dashThreshold && duration < interferenceThreshold {
                        result = "-"
                    } else if duration >= interferenceThreshold {
                        result = "#"
                    }
                } else {
                    if duration <= dashThreshold {
                        result = "" // Przerwa między elementami
                    } else if duration <= characterPauseThreshold {
                        result = " " // Przerwa między znakami
                    } else {
                        result = " / " // Przerwa między słowami
                    }
                }
            }
            currentSignal = signal
            duration = unitTime
            return result
        }
    }
}

// Użycie generatora
let morseGenerator = MorseCodeGenerator()
var output = ""

let signals = [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
for signal in signals {
    if let result = morseGenerator.send(signal: signal) {
        output += result
    }
}

print(output) // Wyświetla zdekodowany kod Morse'a z uwzględnieniem przerw i zakłóceń
