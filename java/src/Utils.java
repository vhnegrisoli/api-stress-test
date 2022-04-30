import java.util.Collection;
import java.util.HashMap;

public class Utils {

    public static boolean isEmpty(Object o) {
        if (o == null) {
            return true;
        }
        if (o instanceof String && o.equals("")) {
            return true;
        }
        if (o instanceof Object[] && ((Object[]) o).length == 0) {
            return true;
        }
        if (o instanceof Collection && ((Collection<?>) o).isEmpty()) {
            return true;
        }
        if (o instanceof HashMap && ((HashMap<?, ?>) o).isEmpty()) {
            return true;
        }
        return false;
    }

}
