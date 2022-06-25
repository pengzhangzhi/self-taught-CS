; (define (over-or-under num1 num2) 'YOUR-CODE-HERE)

; (define (make-adder num) 'YOUR-CODE-HERE)

(define (composed f g)
    (lambda (x) (
        f (g x)
        )
    )
)

(define (square n) (* n n))

(define (pow base exp)

    (cond
        ( (= exp 1) base)
        ((odd? exp) (* base (pow (* base base) (quotient exp 2) ) ) )
        (else (pow (* base base) (quotient exp 2) ) )



    )


)
