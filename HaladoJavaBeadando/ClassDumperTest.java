import org.junit.Test;
import static org.junit.Assert.*;

public class ClassDumperTest {
    @Test
    public void testDump(){
        String expected = "public class TestClass1 extends Thread implements Runnable, Serializable {\n" +
                "\tprivate static final int CONST;\n" +
                "\ttransient volatile boolean flag;\n" +
                "\tprotected Object obj;\n" +
                "\tpublic int n;\n" +
                "\n}";

        String result = ClassDumper.dump(TestClass1.class);

        assertEquals(expected, result);
    }

    //@Test
    /*public void testDump2(){
        String expected = "public class TestClass2 extends java.lang.Thread {\n" +
                "\tprivate static final int CONST;\n" +
                "\ttransient volatile boolean flag;\n" +
                "\tprotected java.lang.Object obj;\n" +
                "\tpublic int n;\n\n" +
                "\tpublic static void printConst(...) { /* method body  }\n}";

       /* String result = ClassDumper.dump(TestClass2.class);

        assertEquals(expected, result);
    } */

}
