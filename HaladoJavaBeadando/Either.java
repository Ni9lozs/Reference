import java.util.NoSuchElementException;
import java.util.function.Function;
import java.util.function.Supplier;

public class Either<L, R> {
    private final L left;
    private final R right;

    private Either(L left, R right){
        this.left = left;
        this.right = right;
    }

    public static <L, R> Either<L, R> left(L value){
        return new Either<>(value, null);
    }

    public static <L,R> Either<L, R> right(R value){
        return new Either<>(null, value);
    }

    public static <T> T iterate(Either<T, T> either, int n, Function<T, T> function) {
        T result = either.right;
        for(int i = 0; i < n; i++) {
            result = function.apply(result);
        }
        return result;
    }

    public Either<R, L> swap(){
        return new Either<>(right, left);
    }

    public boolean isLeft(Either<L, R> e){
        if(e.right == null) return true;
        else return false;
    }

    public boolean isRight(Either<L, R> e){
        if(e.left == null) return true;
        else return false;
    }

    public L getLeft(Either<L, R> e){
        L l = e.left;
        if(isLeft(e)){
            return l;
        } if(isRight(e)){
            throw new NoSuchElementException();
        }
        return l;
    }

    public R getRight(Either<L, R> e){
        R r = e.right;
        if(isRight(e)){
            return r;
        }
        if(isLeft(e)){
            throw new NoSuchElementException();
        }
        return r;
    }

    public R orElseGet(Supplier<R> sr, Either<L, R> e){
        if(isLeft(e)){
            return sr.get();
        } else {
            return right;
        }
    }

    public <T> Either<L, T> map(Function<R, T> function, Either<L, R> e){
        if(isLeft(e)){
            return Either.left(left);
        } else {
            return Either.right(function.apply(right));
        }
    }

    public <T> Either<L, T> bind (Function<R, Either<L, T>> function, Either<L, R> e){
        if(isLeft(e)){
            return Either.left(left);
        } else {
            return function.apply(right);
        }
    }
}
