export function getSimpleName(name) {
    var simpleName;
    switch(name){
        case 'ADVANCED MICRO DEVICES INC' :
            simpleName = 'AMD';
            break;
        case 'Walmart Inc.':
            simpleName = '월마트';
            break;
        case 'NVIDIA CORP':
            simpleName = 'NVIDIA';
            break;
        case 'AMAZON COM INC':
            simpleName = '아마존';
            break;
        case 'Meta Platforms, Inc.':
            simpleName = '메타';
            break;
        case 'BERKSHIRE HATHAWAY INC':
            simpleName = '버크셔해서웨이';
            break;
        case 'Salesforce, Inc.':
            simpleName = '세일즈포스';
            break;
        case 'Mastercard Inc':
            simpleName = '마스터카드';
            break;
        case 'Tesla, Inc.':
            simpleName = '테슬라';
            break;
        case 'AbbVie Inc.':
            simpleName = '애브비';
            break;
        case 'Alphabet Inc.':
            simpleName = '알파벳';
            break;
        case 'JPMORGAN CHASE & CO':
            simpleName = 'JP 모건';
            break;
        case 'JOHNSON & JOHNSON':
            simpleName = '존슨앤존슨';
            break;
        case 'Merck & Co., Inc.':
            simpleName = 'MSD';
            break;
        case 'EXXON MOBIL CORP':
            simpleName = '엑슨모빌';
            break;
        case 'HOME DEPOT, INC.':
            simpleName = '홈디포';
            break;
        case 'ELI LILLY & Co':
            simpleName = '엘리 릴리';
            break;
        case 'BANK OF AMERICA CORP /DE/':
            simpleName = '뱅크오브아메리카';
            break;
        case 'UNITEDHEALTH GROUP INC':
            simpleName = '유나이티드헬스그룹';
            break;
        case 'ORACLE CORP':
            simpleName = '오라클';
            break;
        case 'MICROSOFT CORP':
            simpleName = '마이크로소프트';
            break;
        case 'PROCTER & GAMBLE Co':
            simpleName = '프록터앤갬블';
            break;
        case 'VISA INC.':
            simpleName = '비자';
            break;
        case 'Broadcom Inc.':
            simpleName = '브로드컴';
            break;
        case 'Apple Inc.':
            simpleName = '애플';
            break;
        case 'COSTCO WHOLESALE CORP /NEW':
            simpleName = '코스트코';
            break;
        default:
            simpleName = name;
    }
    return simpleName;
};