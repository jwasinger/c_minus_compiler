import java.util.regex.*;

public class Token {
  private String       value;
  private TokenType    type;
  private String       regex;
  private Pattern      regexPattern;

  public void SetValue(String value) {
    this.value = value;
  }

  public String GetValue() {
    return this.value;
  }

  public void SetType(TokenType type) {
    this.type = type;
  }

  public TokenType GetType() {
    return this.type;
  }
  
  public String GetRegex() {
    return this.regex;
  }

  public void SetRegex(String regex) {
    this.regex = regex;
    this.regexPattern = Pattern.compile("^("+this.regex+")");
  }

  public Pattern GetRegexPattern() {
    return this.regexPattern;
  }


  public Matcher Match(String str) {
    Matcher regexMatcher = this.regexPattern.matcher(str);
    if (regexMatcher.find()) {
      return regexMatcher;
    }
    return null;
  }

  public Token(TokenType type, String value, String regex) {
    this.value = value;
    this.type = type;
    this.regex = regex;
    this.regexPattern = Pattern.compile(this.regex);
  }
}
