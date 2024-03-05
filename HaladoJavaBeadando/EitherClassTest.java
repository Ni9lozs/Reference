import org.junit.jupiter.api.Test;

import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

public class EitherClassTest {
    @Test
    void testEither(){
        Either<String, Integer> leftEither = Either.left("Error");
        Either<String, Integer> rightEither = Either.right(42);

        assertTrue(leftEither.isLeft(leftEither));
        assertTrue(rightEither.isRight(rightEither));

        assertEquals("Error", leftEither.getLeft(leftEither));
        assertEquals(42, rightEither.getRight(rightEither));
    }
}
