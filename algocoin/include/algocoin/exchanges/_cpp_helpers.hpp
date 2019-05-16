#include <iostream>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

#ifndef __ALGOCOIN_LIB_EXCHANGES_CPP_HELPERS_HPP__
#define __ALGOCOIN_LIB_EXCHANGES_CPP_HELPERS_HPP__
void test();

BOOST_PYTHON_MODULE(_cpp_helpers)
{
    boost::python::def("test", test);
}
#endif