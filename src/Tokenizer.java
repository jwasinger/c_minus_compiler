import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.LinkedList;

public class Tokenizer {
  private LinkedList<Token> tokenRules;

  /*
  public Tokenizer() {
    this.tokenRules = new LinkedList<Token>(); 
    
    this.tokenRules.add(new Token(IF, null, "if"));
    this.tokenRules.add(new Token(TYPE_INT, null, "int"));
    this.tokenRules.add(new Token(TYPE_VOID, null, "void"));
    this.tokenRules.add(new Token(INT, null, "[0-9]+"));
    this.tokenRules.add(new Token(ID, null, "[a-zA-Z][a-zA-Z0-9_]*"));
    this.tokenRules.add(new Token(BRACKET_LET, null, "\\]"));
    this.tokenRules.add(new Token(BRACKET_RIGHT, null, "\\["));
    this.tokenRules.add(new Token(BRACE_LEFT, null, "\\}"));
    this.tokenRules.add(new Token(BRACE_RIGHT, null, "\\{"));
    this.tokenRules.add(new Token(SEMI_COLON, null, "\\;"));
    this.tokenRules.add(new Token(ELSE, null, "else"));
    this.tokenRules.add(new Token(ELSE, null, "return"));
    this.tokenRules.add(new Token(ELSE, null, "<="));
  }

  public []Token Scan(String code) {
          
  }

  private void add(String regex, TokenType tokenType) {
    
  }
  */

  public static void main(String[]  args) {
    Pattern space_regex = Pattern.compile("^(\\s)");
    Pattern tab_regex = Pattern.compile("^(\\t)");

    String regex_str = "\\(";
    Pattern regex = Pattern.compile("^("+regex_str+")");
    String str = "\t\t\t((( ((((((((("; 

    while(str.length() != 0) {
      Matcher m = regex.matcher(str);
      if (m.find()) {
        String tok = m.group().trim();

        str = m.replaceFirst("");
        System.out.println(str);
      } else {
        Matcher tab_m = tab_regex.matcher(str);
        if (tab_m.find()) {
          str = tab_m.replaceFirst("");
        }

        Matcher space_m = space_regex.matcher(str);
        if (space_m.find()) {
          str = space_m.replaceFirst("");
        }
      }
    }
  }
}
