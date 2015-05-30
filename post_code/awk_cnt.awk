#!/usr/bin/awk -f
{
    if( NR == 1 )
        dict_code[$NF] = 1

    if( $NF in dict_code )
        dict_code[$NF] = dict_code[$NF] + 1;
    else
        dict_code[$NF] = 1;
}
END{
    for( code in dict_code)
        print code, dict_code[code];
}
        
