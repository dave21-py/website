
FUNCTION Polar(x,y)

    r = sqrt(x^2 + y^2)

    IF x > 0 THEN
        teta = atan(y/x)
    ELSE IF x < 0 THEN
        IF y >0 THEN
            teta = atan(y/x) + pi
        ELSE
            teta = atan(y/x) - pi
        END IF
    ELSE
        IF y > 0 THEN
            teta = pi / 2
        ELSE IF y < 0 THEN
            teta = -pi / 2
        ELSE
            teta = 0
        END IF
    END IF

    teta_in_degrees = teta * 180 / pi

    RETURN r, teta_in_degrees

END FUNCTION




FUNCTION GetTheLetterGrades(numericGrade)

    IF numericGrade >= 90 THEN
        letterGrade = "A"
    ELSE IF numericGrade >= 80 THEN
        letterGrade = "B"
    ELSE IF numericGrade >= 70 THEN
        letterGrade = "C"
    ELSE IF numericGrade >= 60 THEN
        letterGrade = "D"
    ELSE
        letterGrade = "F"
    END IF

    RETURN letterGrade

END FUNCTION