//------------------------------------------------------------------------------
// Copyright (C) 2010, Raditex AB
// All rights reserved.
//
// rSCADA
// http://www.rSCADA.se
// info@rscada.se
//
//------------------------------------------------------------------------------

#include <err.h>
#include <stdio.h>
#include <string.h>

#include <mbus/mbus.h>

int
main(int argc, char *argv[])
{
    FILE *fp = NULL;
    size_t buff_len, len;
    int result, normalized = 0;
    unsigned char raw_buff[4096], buff[4096];
    mbus_frame reply;
    mbus_frame_data frame_data;
    char *xml_result = NULL, *file = NULL;

    // if (argc == 4 && strcmp(argv[1], "-n") == 0)
    // {
    //     file = argv[2];
    //     normalized = 1;
    // }
    // else if (argc == 2)
    // {
    //     file = argv[1];
    // } 
    // else
    // {
    //     fprintf(stderr, "usage: %s [-n] hex-file\n", argv[0]);
    //     fprintf(stderr, "    optional flag -n for normalized values\n");
    //     return 1;
    // }

    memset(raw_buff, 0, sizeof(raw_buff));
    memcpy(raw_buff, argv[2],strlen(argv[2]));
    
    // fprintf(stderr, "%s", argv[1]);
    // putc(*raw_buff, stdout);

    buff_len = mbus_hex2bin(buff,sizeof(buff),raw_buff,sizeof(raw_buff));

    memset(&reply, 0, sizeof(reply));
    memset(&frame_data, 0, sizeof(frame_data));

    //mbus_parse_set_debug(1);

    result = mbus_parse(&reply, buff, buff_len);

    // printf("\n **************** mbus_parse **************** : \n");
    // mbus_frame_print(&reply);
    
    if (result < 0)
    {
        fprintf(stderr, "mbus_parse: %s\n", mbus_error_str());
        return 1;
    }
    else if (result > 0)
    {
        fprintf(stderr, "mbus_parse: need %d more bytes\n", result);
        return 1;
    }

    result = mbus_frame_data_parse(&reply, &frame_data);

    if (result != 0)
    {
        mbus_frame_print(&reply);
        fprintf(stderr, "mbus_frame_data_parse: %s\n", mbus_error_str());
        return 1;
    }
    
    // printf("\n **************** mbus_frame_data_parse **************** : \n");
    // mbus_frame_print(&reply);
    
    if( strcmp(argv[1], "raw") == 0){
        // process the raw file and print raw output 
        mbus_frame_data_print(&frame_data);
    }


    xml_result = normalized ? mbus_frame_data_xml_normalized(&frame_data) : mbus_frame_data_xml(&frame_data);

    if (xml_result == NULL)
    {
        fprintf(stderr, "Failed to generate XML representation of MBUS frame: %s\n", mbus_error_str());
        return 1;
    }

    // printf("\n ******** mbus_frame_data_xml ********: \n ");
    if( strcmp(argv[1], "xml") == 0){
        // process the raw file and print raw output 
        printf("%s", xml_result);
    }
    
    free(xml_result); 

    mbus_data_record_free(frame_data.data_var.record);

    return 0;
}

