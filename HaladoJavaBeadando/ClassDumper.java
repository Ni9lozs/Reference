import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.stream.Collectors;

public class ClassDumper {
    public static String dump(Class<?> classs) {
        String mod = Modifier.toString(classs.getModifiers());
        String cn = classs.getSimpleName();
        String sc = classs.getSuperclass().getSimpleName();
        String i = Arrays.stream(classs.getInterfaces()).map(Class::getSimpleName).collect(Collectors.joining(", "));

        StringBuilder sb = new StringBuilder();

        sb.append(mod + " ");
        sb.append("class " + cn);
        if (!sc.equals("Object")) sb.append(" extends " + sc);
        if (!i.isEmpty()) sb.append(" implements " + i);
        sb.append(" {\n");

        Field[] f = classs.getDeclaredFields();
        for(Field fs : f) {
            String fm = Modifier.toString(fs.getModifiers());
            String ft = fs.getType().getSimpleName();
            String fn = fs.getName();
            sb.append("\t" + fm + " ");
            sb.append(ft + " " + fn + ";\n");
        }

        sb.append("\n}");

        return sb.toString();
    }
}
