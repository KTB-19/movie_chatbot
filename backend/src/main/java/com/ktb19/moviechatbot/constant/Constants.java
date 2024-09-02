package com.ktb19.moviechatbot.constant;

public final class Constants {

    public final static String PATTERN_REGEXP_ALL = "^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9 !#$%&'*+/=?`{(|)}~^.-:]*$";
    public final static String PATTERN_REGEXP_ALL_MESSAGE = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다.";
    public final static String PATTERN_REGEXP_KOREAN = "^[가-힣 ]*$";
    public final static String PATTERN_REGEXP_KOREAN_MESSAGE = "한글, 띄어쓰기만 입력할 수 있습니다.";
    public final static String PATTERN_JSONFORMAT_DATE = "yyyy-MM-dd";
    public final static String PATTERN_JSONFORMAT_TIME = "HH:mm";

}
