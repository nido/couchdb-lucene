package com.github.rnewson.couchdb.lucene.util;

/**
 * Copyright 2009 Robert Newson
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); 
 * you may not use this file except in compliance with the License. 
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0 
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import static com.github.rnewson.couchdb.lucene.util.ServletUtils.getBooleanParameter;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.log4j.Logger;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.Field.Store;

public class Utils {

    public static Logger getLogger(final Class clazz, final String suffix) {
        return Logger.getLogger(clazz.getCanonicalName() + "." + suffix);
    }

    public static void setResponseContentTypeAndEncoding(final HttpServletRequest req, final HttpServletResponse resp) {
        final String accept = req.getHeader("Accept");
        if (getBooleanParameter(req, "force_json") || (accept != null && accept.contains("application/json"))) {
            resp.setContentType("application/json");
        } else {
            resp.setContentType("text/plain");
        }
        resp.setCharacterEncoding("utf-8");
    }

    public static Field text(final String name, final String value, final boolean store) {
        return new Field(name, value, store ? Store.YES : Store.NO, Field.Index.ANALYZED);
    }

    public static Field token(final String name, final String value, final boolean store) {
        return new Field(name, value, store ? Store.YES : Store.NO, Field.Index.NOT_ANALYZED_NO_NORMS);
    }

    public static String urlEncode(final String path) {
        try {
            return URLEncoder.encode(path, "UTF-8");
        } catch (final UnsupportedEncodingException e) {
            throw new Error("UTF-8 support missing!");
        }
    }

}